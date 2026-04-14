"""
SynapsIA — Report Generator (Layer 3 — Execution)
Deterministic script: pipeline results → brain map images + JSON report + PDF

Generates:
  - glass_brain.png    : nilearn glass brain view
  - axial.png          : axial brain slice
  - coronal.png        : coronal brain slice
  - sagittal.png       : sagittal brain slice
  - report.json        : structured pre-report
  - relatorio.pdf      : exportable medical PDF
"""
import os
import json
import numpy as np
from datetime import datetime

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend — required for server-side rendering
    import matplotlib.pyplot as plt
    from nilearn import plotting, datasets, image
    NILEARN_AVAILABLE = True
except ImportError:
    NILEARN_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
        Table, TableStyle, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ──────────────────────────────────────────────────────────────────────────────
# Brain image generation
# ──────────────────────────────────────────────────────────────────────────────

def _generate_simulated_stat_map(exam_dir: str):
    """
    Creates a fake statistical map image for simulated/demo mode.
    Returns path to a generated placeholder PNG.
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(figsize=(8, 4), facecolor="#0a0a0f")
    ax.set_facecolor("#0d1117")

    # Draw a simple brain outline placeholder
    theta = np.linspace(0, 2 * np.pi, 300)
    x_brain = 3.5 * np.cos(theta) * (1 + 0.15 * np.cos(6 * theta))
    y_brain = 2.8 * np.sin(theta) * (1 + 0.1 * np.sin(4 * theta))
    ax.fill(x_brain, y_brain, color="#1a1f2e", zorder=1)
    ax.plot(x_brain, y_brain, color="#4f8ef7", linewidth=1.5, zorder=2)

    # Scatter hot spots
    rng = np.random.default_rng(42)
    n_spots = 12
    spot_x = rng.uniform(-2.5, 2.5, n_spots)
    spot_y = rng.uniform(-1.8, 2.0, n_spots)
    spot_v = rng.uniform(0.3, 1.0, n_spots)
    sc = ax.scatter(spot_x, spot_y, c=spot_v, cmap="cool", s=120,
                    alpha=0.85, vmin=0, vmax=1, zorder=3)
    plt.colorbar(sc, ax=ax, label="Desvio z-score", fraction=0.02)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-4, 4)
    ax.axis("off")
    ax.set_title("Mapa de Ativação Cerebral (simulado)", color="#a855f7",
                 fontsize=11, pad=8)

    path = os.path.join(exam_dir, "images", "brain_map.png")
    plt.savefig(path, dpi=120, bbox_inches="tight",
                facecolor="#0a0a0f", edgecolor="none")
    plt.close(fig)
    return path


def _generate_connectivity_heatmap(conn_matrix: list, region_names: list, exam_dir: str) -> str:
    """Plots the functional connectivity matrix as a heatmap"""
    fig, ax = plt.subplots(figsize=(9, 8), facecolor="#0a0a0f")
    ax.set_facecolor("#0d1117")

    matrix = np.array(conn_matrix)
    n = min(matrix.shape[0], 20)
    matrix = matrix[:n, :n]
    short_names = [r.split("_")[-1][:12] if "_" in r else r[:12] for r in region_names[:n]]

    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    plt.colorbar(im, ax=ax, fraction=0.03, label="Correlação")

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(short_names, rotation=45, ha="right",
                       fontsize=6.5, color="#94a3b8")
    ax.set_yticklabels(short_names, fontsize=6.5, color="#94a3b8")
    ax.set_title("Matriz de Conectividade Funcional", color="#4f8ef7",
                 fontsize=13, pad=10)

    for spine in ax.spines.values():
        spine.set_edgecolor("#1e293b")

    path = os.path.join(exam_dir, "images", "connectivity.png")
    plt.savefig(path, dpi=120, bbox_inches="tight",
                facecolor="#0a0a0f", edgecolor="none")
    plt.close(fig)
    return path


def _generate_zscore_bar(z_scores: list, region_names: list, exam_dir: str) -> str:
    """Horizontal bar chart of z-scores per brain region"""
    n = min(len(z_scores), 20)
    z = np.array(z_scores[:n])
    names = [r.split("_")[-1][:16] if "_" in str(r) else str(r)[:16] for r in region_names[:n]]

    colors_bar = ["#ef4444" if abs(v) > 2.0 else "#4f8ef7" for v in z]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#0a0a0f")
    ax.set_facecolor("#0d1117")
    bars = ax.barh(names, z, color=colors_bar, edgecolor="#1e293b", height=0.7)
    ax.axvline(x=2.0, color="#f59e0b", linestyle="--", linewidth=1, alpha=0.7, label="Limiar z=2.0")
    ax.axvline(x=-2.0, color="#f59e0b", linestyle="--", linewidth=1, alpha=0.7)
    ax.axvline(x=0, color="#475569", linewidth=0.8)
    ax.set_xlabel("Z-score de Desvio", color="#94a3b8")
    ax.set_title("Desvio por Região Cerebral", color="#4f8ef7", fontsize=13, pad=10)
    ax.tick_params(colors="#94a3b8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for spine in ax.spines.values():
        spine.set_edgecolor("#1e293b")
    ax.legend(facecolor="#0d1117", labelcolor="#94a3b8", edgecolor="#1e293b")

    path = os.path.join(exam_dir, "images", "zscore_chart.png")
    plt.savefig(path, dpi=120, bbox_inches="tight",
                facecolor="#0a0a0f", edgecolor="none")
    plt.close(fig)
    return path


def _generate_nilearn_brain_plots(pipeline_results: dict, exam_dir: str) -> dict:
    """
    Try to generate nilearn glass brain and stat map plots.
    Falls back to simulated plots if atlas/data unavailable.
    """
    images = {}

    if not NILEARN_AVAILABLE:
        images["brain_map"] = _generate_simulated_stat_map(exam_dir)
        return images

    try:
        # Glass brain using a standard MNI152 template
        template = datasets.load_mni152_template(resolution=2)
        output_types = [
            ("glass_brain", "glass brain"),
        ]
        # Glass brain view
        gb_path = os.path.join(exam_dir, "images", "glass_brain.png")
        fig = plotting.plot_glass_brain(
            None,
            display_mode="lyrz",
            title="Glass Brain — Redes Neurais Funcionais",
            figure=plt.figure(figsize=(14, 4), facecolor="#0a0a0f"),
            colorbar=False,
            black_bg=True,
        )
        fig.savefig(gb_path, dpi=120, bbox_inches="tight",
                    facecolor="#0a0a0f")
        plotting.close()
        images["glass_brain"] = gb_path

        # Axial slice
        ax_path = os.path.join(exam_dir, "images", "axial.png")
        d = plotting.plot_anat(
            template, display_mode="z", cut_coords=[-20, 0, 20, 40],
            black_bg=True, title="Corte Axial",
            figure=plt.figure(figsize=(12, 3), facecolor="#0a0a0f"),
        )
        d.savefig(ax_path, dpi=120, bbox_inches="tight", facecolor="#0a0a0f")
        plotting.close()
        images["axial"] = ax_path

        # Coronal slice
        cor_path = os.path.join(exam_dir, "images", "coronal.png")
        d = plotting.plot_anat(
            template, display_mode="y", cut_coords=[-40, -20, 0, 20],
            black_bg=True, title="Corte Coronal",
            figure=plt.figure(figsize=(12, 3), facecolor="#0a0a0f"),
        )
        d.savefig(cor_path, dpi=120, bbox_inches="tight", facecolor="#0a0a0f")
        plotting.close()
        images["coronal"] = cor_path

        # Sagittal slice
        sag_path = os.path.join(exam_dir, "images", "sagittal.png")
        d = plotting.plot_anat(
            template, display_mode="x", cut_coords=[-40, -20, 0, 20],
            black_bg=True, title="Corte Sagital",
            figure=plt.figure(figsize=(12, 3), facecolor="#0a0a0f"),
        )
        d.savefig(sag_path, dpi=120, bbox_inches="tight", facecolor="#0a0a0f")
        plotting.close()
        images["sagittal"] = sag_path

    except Exception as exc:
        print(f"[SynapsIA] nilearn plot error: {exc} — using simulated brain map")
        images["brain_map"] = _generate_simulated_stat_map(exam_dir)

    return images


# ──────────────────────────────────────────────────────────────────────────────
# Report assembly
# ──────────────────────────────────────────────────────────────────────────────

def _anomaly_level(score: float) -> str:
    if score < 0.33:
        return "Baixo"
    elif score < 0.66:
        return "Moderado"
    return "Alto"


def _build_recommendations(affected_regions: list, anomaly_score: float) -> list:
    """Generate structured clinical recommendations based on findings"""
    recs = [
        "Este pré-relatório deve ser validado por um neurologista ou neurorradiologista habilitado.",
        "Comparação com exames anteriores é recomendada para avaliação de progressão.",
    ]
    if anomaly_score > 0.66:
        recs += [
            "Score de anomalia elevado — considere avaliação neurológica urgente.",
            "Avaliação neuropsicológica complementar pode ser indicada.",
        ]
    elif anomaly_score > 0.33:
        recs += [
            "Score de anomalia moderado — acompanhamento periódico recomendado.",
            "Correlacionar achados com quadro clínico do paciente.",
        ]
    else:
        recs.append("Score de anomalia baixo — padrão próximo ao esperado para a faixa etária.")

    high_regions = [r for r in affected_regions if r.get("deviation") == "alta"]
    if high_regions:
        names = ", ".join([r["name"] for r in high_regions[:3]])
        recs.append(f"Atenção especial às regiões com desvio elevado: {names}.")

    return recs


def generate_report(pipeline_results: dict, exam_dir: str) -> dict:
    """
    Assembles the full pre-report:
     - Generates brain map images
     - Builds connectivity heatmap and z-score chart
     - Constructs structured JSON report
    """
    images_dir = os.path.join(exam_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Generate all visual assets
    brain_images = _generate_nilearn_brain_plots(pipeline_results, exam_dir)

    if pipeline_results.get("connectivity_matrix") and pipeline_results.get("region_names"):
        conn_path = _generate_connectivity_heatmap(
            pipeline_results["connectivity_matrix"],
            pipeline_results["region_names"],
            exam_dir,
        )
        brain_images["connectivity"] = conn_path

    if pipeline_results.get("z_scores") and pipeline_results.get("region_names"):
        zs_path = _generate_zscore_bar(
            pipeline_results["z_scores"],
            pipeline_results["region_names"],
            exam_dir,
        )
        brain_images["zscore_chart"] = zs_path

    affected_regions = pipeline_results.get("affected_regions", [])
    anomaly_score = pipeline_results.get("anomaly_score", 0.0)

    # Image paths relative to /uploads (served statically)
    exam_id = os.path.basename(exam_dir)
    image_urls = {
        k: f"/uploads/{exam_id}/images/{os.path.basename(v)}"
        for k, v in brain_images.items()
    }

    report = {
        "exam_id": exam_id,
        "exam_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "processing_time_seconds": pipeline_results.get("processing_time_seconds", 0),
        "is_simulated": pipeline_results.get("simulated", False),
        "n_volumes": pipeline_results.get("n_volumes", 0),
        "n_regions_analyzed": pipeline_results.get("n_regions", 0),
        "mean_connectivity": pipeline_results.get("mean_connectivity", 0),
        "affected_regions": affected_regions,
        "anomaly_score": anomaly_score,
        "anomaly_level": _anomaly_level(anomaly_score),
        "recommendations": _build_recommendations(affected_regions, anomaly_score),
        "images": image_urls,
        "disclaimer": (
            "Este pré-relatório foi gerado por inteligência artificial e deve ser "
            "validado por um profissional médico habilitado. "
            "O médico é sempre responsável pelo diagnóstico final."
        ),
    }

    # Persist report JSON to disk
    report_path = os.path.join(exam_dir, "report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report


# ──────────────────────────────────────────────────────────────────────────────
# PDF Export
# ──────────────────────────────────────────────────────────────────────────────

def generate_pdf(report: dict, exam_dir: str) -> str:
    """
    Generates a clean medical PDF from the structured report.
    Returns the path to the generated PDF file.
    """
    pdf_path = os.path.join(exam_dir, "relatorio_synapsia.pdf")

    if not REPORTLAB_AVAILABLE:
        # Fallback: write a plain-text report
        txt_path = pdf_path.replace(".pdf", ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("SYNAPSIA — PRÉ-RELATÓRIO NEUROLÓGICO\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Data: {report.get('exam_date', '')}\n")
            f.write(f"Tempo de processamento: {report.get('processing_time_seconds', 0)}s\n\n")
            f.write(f"Score de Anomalia: {report.get('anomaly_score', 0)} — {report.get('anomaly_level', '')}\n\n")
            f.write("REGIÕES AFETADAS:\n")
            for r in report.get("affected_regions", []):
                f.write(f"  - {r['name']} (z={r['z_score']}, desvio={r['deviation']})\n")
            f.write("\nRECOMENDAÇÕES:\n")
            for rec in report.get("recommendations", []):
                f.write(f"  • {rec}\n")
            f.write(f"\n{'=' * 60}\n{report.get('disclaimer', '')}\n")
        return txt_path

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # Style palette
    DARK = colors.HexColor("#0a0a0f")
    BLUE = colors.HexColor("#4f8ef7")
    PURPLE = colors.HexColor("#a855f7")
    LIGHT = colors.HexColor("#e2e8f0")
    MUTED = colors.HexColor("#94a3b8")
    WARNING = colors.HexColor("#f59e0b")
    RED = colors.HexColor("#ef4444")
    GREEN = colors.HexColor("#22c55e")

    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        "SynTitle", parent=styles["Title"],
        fontSize=22, textColor=BLUE, spaceAfter=4,
        alignment=TA_CENTER, fontName="Helvetica-Bold",
    )
    style_subtitle = ParagraphStyle(
        "SynSub", parent=styles["Normal"],
        fontSize=10, textColor=MUTED, spaceAfter=2,
        alignment=TA_CENTER,
    )
    style_section = ParagraphStyle(
        "SynSection", parent=styles["Heading2"],
        fontSize=13, textColor=PURPLE, spaceBefore=14, spaceAfter=6,
        fontName="Helvetica-Bold",
    )
    style_body = ParagraphStyle(
        "SynBody", parent=styles["Normal"],
        fontSize=9.5, textColor=LIGHT, spaceAfter=4, leading=14,
        alignment=TA_JUSTIFY,
    )
    style_warning = ParagraphStyle(
        "SynWarn", parent=styles["Normal"],
        fontSize=9, textColor=WARNING, spaceAfter=6,
        borderColor=WARNING, borderWidth=1, borderPadding=8,
        backColor=colors.HexColor("#1a1407"),
        leading=14,
    )
    style_small = ParagraphStyle(
        "SynSmall", parent=styles["Normal"],
        fontSize=8, textColor=MUTED,
    )

    story = []

    # Header
    story.append(Paragraph("SynapsIA", style_title))
    story.append(Paragraph("Assistente Diagnóstico Neurológico com IA", style_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=10))

    # Disclaimer box
    story.append(Paragraph(
        f"⚠ {report.get('disclaimer', '')}", style_warning
    ))

    # Exam metadata table
    story.append(Paragraph("Informações do Exame", style_section))
    meta_data = [
        ["Data do Exame", report.get("exam_date", "—")],
        ["Tempo de Processamento", f"{report.get('processing_time_seconds', 0):.1f} segundos"],
        ["Volumes Analisados", str(report.get("n_volumes", "—"))],
        ["Regiões Analisadas", str(report.get("n_regions_analyzed", "—"))],
        ["Conectividade Média", f"{report.get('mean_connectivity', 0):.4f}"],
        ["Modo de Processamento", "Simulado (demo)" if report.get("is_simulated") else "Real"],
    ]
    meta_table = Table(meta_data, colWidths=[5.5 * cm, 12 * cm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0d1117")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#111827")),
        ("TEXTCOLOR", (0, 0), (0, -1), BLUE),
        ("TEXTCOLOR", (1, 0), (1, -1), LIGHT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#0d1117"), colors.HexColor("#111827")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1e293b")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)

    # Anomaly score
    story.append(Paragraph("Score de Anomalia", style_section))
    score = report.get("anomaly_score", 0)
    level = report.get("anomaly_level", "—")
    level_color = RED if level == "Alto" else (WARNING if level == "Moderado" else GREEN)
    score_data = [["Score", "Nível de Risco"],
                  [f"{score:.3f} / 1.000", level]]
    score_table = Table(score_data, colWidths=[8.75 * cm, 8.75 * cm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d1117")),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#111827")),
        ("TEXTCOLOR", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 1), (0, 1), LIGHT),
        ("TEXTCOLOR", (1, 1), (1, 1), level_color),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1e293b")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(score_table)

    # Affected regions
    story.append(Paragraph("Regiões Cerebrais Afetadas", style_section))
    affected = report.get("affected_regions", [])
    if affected:
        region_data = [["Região", "Z-Score", "Desvio", "Lateralidade"]]
        for r in affected:
            z = r.get("z_score", 0)
            dev = r.get("deviation", "—")
            dev_display = "Alta" if dev == "alta" else "Moderada"
            region_data.append([
                r.get("name", "—"),
                f"{z:.3f}",
                dev_display,
                r.get("laterality", "—").capitalize(),
            ])
        region_table = Table(region_data, colWidths=[8 * cm, 3 * cm, 3.5 * cm, 3 * cm])
        region_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e1b4b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), BLUE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TEXTCOLOR", (0, 1), (-1, -1), LIGHT),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.HexColor("#0d1117"), colors.HexColor("#111827")
            ]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1e293b")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(region_table)
    else:
        story.append(Paragraph("Nenhuma região com desvio significativo identificada.", style_body))

    # Brain map images
    story.append(Paragraph("Mapas Cerebrais", style_section))
    image_paths_on_disk = {}
    for key, url in report.get("images", {}).items():
        # Convert URL back to local path
        # URL: /uploads/{exam_id}/images/{filename}
        parts = url.split("/")
        if len(parts) >= 4:
            local_path = os.path.join(exam_dir, "images", parts[-1])
            if os.path.exists(local_path):
                image_paths_on_disk[key] = local_path

    for key, img_path in image_paths_on_disk.items():
        try:
            img = RLImage(img_path, width=17 * cm, height=6 * cm,
                          kind="proportional")
            story.append(img)
            story.append(Spacer(1, 0.3 * cm))
        except Exception:
            pass

    # Recommendations
    story.append(Paragraph("Recomendações Clínicas", style_section))
    for i, rec in enumerate(report.get("recommendations", []), 1):
        story.append(Paragraph(f"{i}. {rec}", style_body))

    # Footer
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED))
    story.append(Paragraph(
        "SynapsIA © 2025 — Assistente Diagnóstico Neurológico com IA | "
        "Uso exclusivo por profissionais de saúde habilitados.",
        style_small,
    ))

    doc.build(story)
    return pdf_path
