"""
SynapsIA — Exam Routes
Handles fMRI file upload, processing status polling, and PDF export
"""
import os
import uuid
import asyncio
import shutil
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from processing.fmri_pipeline import process_fmri
from processing.report_generator import generate_report, generate_pdf

router = APIRouter()

# In-memory store for exam results — MVP (no DB required)
# key: exam_id (str), value: dict with status/progress/report
exam_store: dict = {}

ALLOWED_EXTENSIONS = (".nii", ".nii.gz")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "temp_uploads")


def _is_valid_extension(filename: str) -> bool:
    """Check if filename ends with an allowed NIfTI extension"""
    return filename.endswith(".nii.gz") or filename.endswith(".nii")


async def _run_processing(exam_id: str, file_path: str, exam_dir: str):
    """
    Background task: runs the full fMRI processing pipeline
    Updates exam_store with progress and final report
    """
    try:
        # Phase 1 — loading
        exam_store[exam_id].update({
            "progress": 25,
            "phase": 1,
            "message": "Carregando exame..."
        })
        await asyncio.sleep(0.5)  # allow event loop to breathe

        # Phase 2 — neural analysis (blocking CPU work in thread)
        exam_store[exam_id].update({
            "progress": 55,
            "phase": 2,
            "message": "Analisando redes neurais..."
        })
        loop = asyncio.get_event_loop()
        pipeline_results = await loop.run_in_executor(
            None, process_fmri, file_path, exam_dir
        )

        # Phase 3 — report generation
        exam_store[exam_id].update({
            "progress": 80,
            "phase": 3,
            "message": "Gerando pré-relatório..."
        })
        report = await loop.run_in_executor(
            None, generate_report, pipeline_results, exam_dir
        )

        # Done
        exam_store[exam_id].update({
            "status": "completed",
            "progress": 100,
            "message": "Pré-relatório concluído",
            "report": report,
        })

    except Exception as exc:
        exam_store[exam_id].update({
            "status": "error",
            "progress": 0,
            "message": f"Erro durante o processamento: {str(exc)}",
        })


@router.post("/upload")
async def upload_exam(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """
    Accepts a .nii or .nii.gz file, saves it, and starts async processing.
    Returns exam_id for subsequent status polling.
    """
    if not _is_valid_extension(file.filename):
        raise HTTPException(
            status_code=422,
            detail="Formato inválido. Envie arquivos .nii ou .nii.gz"
        )

    exam_id = str(uuid.uuid4())
    exam_dir = os.path.join(UPLOAD_DIR, exam_id)
    images_dir = os.path.join(exam_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Save file to disk
    file_path = os.path.join(exam_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Register exam in store
    exam_store[exam_id] = {
        "status": "processing",
        "progress": 10,
        "phase": 1,
        "message": "Carregando exame...",
        "filename": file.filename,
        "uploaded_at": datetime.now().isoformat(),
    }

    # Kick off background processing
    background_tasks.add_task(_run_processing, exam_id, file_path, exam_dir)

    return {"exam_id": exam_id, "status": "processing"}


@router.get("/status/{exam_id}")
async def get_status(exam_id: str):
    """
    Poll this endpoint to get current processing status.
    Returns: status, progress (0-100), message, and report (when complete).
    """
    if exam_id not in exam_store:
        raise HTTPException(status_code=404, detail="Exame não encontrado")

    entry = exam_store[exam_id]
    response = {
        "status": entry["status"],
        "progress": entry["progress"],
        "message": entry.get("message", ""),
    }

    if entry["status"] == "completed":
        response["report"] = entry["report"]

    return response


@router.get("/result/{exam_id}")
async def get_result(exam_id: str):
    """Returns the full pre-report JSON once processing is complete"""
    if exam_id not in exam_store:
        raise HTTPException(status_code=404, detail="Exame não encontrado")

    entry = exam_store[exam_id]
    if entry["status"] != "completed":
        raise HTTPException(status_code=202, detail="Processamento em andamento")

    return entry["report"]


@router.get("/export-pdf/{exam_id}")
async def export_pdf(exam_id: str):
    """Generates and returns the medical pre-report as a PDF file"""
    if exam_id not in exam_store:
        raise HTTPException(status_code=404, detail="Exame não encontrado")

    entry = exam_store[exam_id]
    if entry["status"] != "completed":
        raise HTTPException(status_code=202, detail="Processamento em andamento")

    exam_dir = os.path.join(UPLOAD_DIR, exam_id)
    pdf_path = generate_pdf(entry["report"], exam_dir)

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"synapsia_relatorio_{exam_id[:8]}.pdf",
    )
