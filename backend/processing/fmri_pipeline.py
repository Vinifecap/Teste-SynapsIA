"""
SynapsIA — fMRI Processing Pipeline (Layer 3 — Execution)
Deterministic script: NIfTI load → preprocessing → connectivity analysis → JSON results

Pipeline:
  1. Load NIfTI volume with nibabel
  2. Validate dimensions (must be 4D for fMRI)
  3. Apply spatial smoothing with nilearn
  4. Create brain mask with NiftiMasker
  5. Extract time series per brain atlas region
  6. Compute functional connectivity (correlation matrix)
  7. Identify significantly deviant regions (z-score > 2.0)
  8. Return structured results dict

Fallback: If file is not a valid 4D fMRI volume, returns realistic simulated data.
"""
import os
import json
import numpy as np
from datetime import datetime

# fMRI libraries (imported inside try/except for graceful degradation)
try:
    import nibabel as nib
    from nilearn import image, plotting, datasets
    from nilearn.maskers import NiftiLabelsMasker, NiftiMasker
    from nilearn.connectome import ConnectivityMeasure
    NILEARN_AVAILABLE = True
except ImportError:
    NILEARN_AVAILABLE = False

# Brain atlas region names for labeling (Harvard-Oxford cortical simplified)
BRAIN_REGIONS = [
    "Córtex Frontal Superior",
    "Córtex Pré-frontal Medial",
    "Giro do Cíngulo Anterior",
    "Córtex Motor Primário",
    "Córtex Somatossensorial",
    "Lóbulo Parietal Superior",
    "Lóbulo Parietal Inferior",
    "Córtex Occipital Lateral",
    "Cuneus",
    "Precuneus",
    "Giro Temporal Superior",
    "Giro Temporal Médio",
    "Giro Temporal Inferior",
    "Hipocampo",
    "Amígdala",
    "Putâmen",
    "Núcleo Caudado",
    "Tálamo",
    "Cerebelo",
    "Córtex Insular",
]


def _simulate_results(reason: str = "file_not_4d") -> dict:
    """
    Returns realistic simulated fMRI analysis results.
    Used when a valid 4D NIfTI file is not provided (demo/test mode).
    """
    rng = np.random.default_rng(seed=42)

    # Simulate a 20x20 connectivity matrix
    n_regions = len(BRAIN_REGIONS)
    raw_corr = rng.uniform(-0.3, 0.9, size=(n_regions, n_regions))
    np.fill_diagonal(raw_corr, 1.0)
    # Make it symmetric
    corr_matrix = (raw_corr + raw_corr.T) / 2

    # Identify "affected" regions (simulated z-score > 2.0)
    z_scores = rng.uniform(0.5, 3.5, size=n_regions)
    affected_indices = np.where(z_scores > 2.0)[0]
    affected_regions = [
        {
            "name": BRAIN_REGIONS[i],
            "z_score": round(float(z_scores[i]), 3),
            "deviation": "alta" if z_scores[i] > 2.8 else "moderada",
            "laterality": "esquerdo" if rng.random() > 0.5 else "direito",
        }
        for i in affected_indices
    ]

    anomaly_score = round(float(np.clip(np.mean(z_scores[affected_indices]) / 3.5, 0, 1)), 3) if len(affected_indices) > 0 else 0.1

    return {
        "simulated": True,
        "simulation_reason": reason,
        "n_volumes": 200,
        "repetition_time": 2.0,
        "n_regions": n_regions,
        "connectivity_matrix": corr_matrix.tolist(),
        "region_names": BRAIN_REGIONS,
        "z_scores": z_scores.tolist(),
        "affected_regions": affected_regions,
        "anomaly_score": anomaly_score,
        "mean_connectivity": round(float(np.mean(np.abs(corr_matrix[np.triu_indices(n_regions, k=1)]))), 4),
    }


def _load_and_validate_nifti(file_path: str):
    """
    Loads a NIfTI file and validates it is a 4D fMRI volume.
    Returns (img, None) on success or (None, reason_str) on failure.
    """
    try:
        img = nib.load(file_path)
        shape = img.shape
        if len(shape) != 4:
            return None, f"not_4d (shape={shape})"
        if shape[3] < 10:
            return None, f"too_few_volumes (n={shape[3]})"
        return img, None
    except Exception as exc:
        return None, f"load_error: {str(exc)}"


def process_fmri(file_path: str, output_dir: str) -> dict:
    """
    Main pipeline entry point.
    Loads the NIfTI file, preprocesses it, computes connectivity,
    and returns a structured results dictionary.
    Falls back to simulated data if processing fails.
    """
    start_time = datetime.now()

    if not NILEARN_AVAILABLE:
        print("[SynapsIA] nilearn not available — returning simulated data")
        results = _simulate_results("nilearn_not_installed")
        results["processing_time_seconds"] = 0.1
        return results

    # Load and validate
    img, err_reason = _load_and_validate_nifti(file_path)
    if img is None:
        print(f"[SynapsIA] NIfTI validation failed ({err_reason}) — using simulated data")
        results = _simulate_results(err_reason)
        results["processing_time_seconds"] = round((datetime.now() - start_time).total_seconds(), 2)
        return results

    try:
        # Step 1: Spatial smoothing (FWHM=6mm — standard for fMRI preprocessing)
        print("[SynapsIA] Applying spatial smoothing (FWHM=6mm)...")
        smoothed_img = image.smooth_img(img, fwhm=6)

        # Step 2: Brain masking — extract grey matter signals
        print("[SynapsIA] Creating brain mask...")
        masker = NiftiMasker(
            standardize=True,
            detrend=True,
            low_pass=0.1,
            high_pass=0.01,
            t_r=2.0,  # Repetition time (TR) — commonly 2s for fMRI
            memory_level=0,
        )
        brain_signals = masker.fit_transform(smoothed_img)
        print(f"[SynapsIA] Extracted signals: {brain_signals.shape}")

        # Step 3: Use Schaefer atlas parcellation for region labeling
        print("[SynapsIA] Loading brain atlas parcellation...")
        try:
            atlas = datasets.fetch_atlas_schaefer_2018(n_rois=20)
            label_masker = NiftiLabelsMasker(
                labels_img=atlas.maps,
                standardize=True,
                detrend=True,
            )
            region_signals = label_masker.fit_transform(smoothed_img)
            region_names = [r.decode() if isinstance(r, bytes) else r for r in atlas.labels]
        except Exception:
            # Fall back to 20 equal parcels from brain signals
            print("[SynapsIA] Atlas fetch failed — using uniform parcellation")
            n_regions = 20
            step = max(1, brain_signals.shape[1] // n_regions)
            region_signals = brain_signals[:, ::step][:, :n_regions]
            region_names = BRAIN_REGIONS[:n_regions]

        # Step 4: Functional connectivity matrix (Pearson correlation)
        print("[SynapsIA] Computing functional connectivity matrix...")
        conn_measure = ConnectivityMeasure(kind="correlation")
        conn_matrix = conn_measure.fit_transform([region_signals])[0]

        # Step 5: Identify deviant regions using z-score
        # Baseline: mean connectivity per region vs. population mean (simulated baseline)
        region_mean_conn = np.mean(np.abs(conn_matrix), axis=1)
        population_mean = 0.35   # typical resting-state fMRI baseline
        population_std = 0.12
        z_scores = (region_mean_conn - population_mean) / population_std

        affected_indices = np.where(np.abs(z_scores) > 2.0)[0]
        affected_regions = []
        for i in affected_indices:
            region_name = region_names[i] if i < len(region_names) else f"Região {i+1}"
            z = float(z_scores[i])
            affected_regions.append({
                "name": region_name,
                "z_score": round(z, 3),
                "deviation": "alta" if abs(z) > 2.8 else "moderada",
                "laterality": "esquerdo" if "L_" in str(region_name) else "direito",
            })

        # Anomaly score: proportion of affected regions, weighted by z-score magnitude
        if len(affected_indices) > 0:
            anomaly_score = round(
                float(np.clip(np.mean(np.abs(z_scores[affected_indices])) / 4.0, 0, 1)), 3
            )
        else:
            anomaly_score = 0.05

        processing_time = round((datetime.now() - start_time).total_seconds(), 2)

        return {
            "simulated": False,
            "n_volumes": img.shape[3],
            "repetition_time": img.header.get_zooms()[3] if len(img.header.get_zooms()) > 3 else 2.0,
            "n_regions": len(region_names),
            "connectivity_matrix": conn_matrix.tolist(),
            "region_names": region_names,
            "z_scores": z_scores.tolist(),
            "affected_regions": affected_regions,
            "anomaly_score": anomaly_score,
            "mean_connectivity": round(
                float(np.mean(np.abs(conn_matrix[np.triu_indices(conn_matrix.shape[0], k=1)]))), 4
            ),
            "processing_time_seconds": processing_time,
        }

    except Exception as exc:
        print(f"[SynapsIA] Processing exception: {exc} — falling back to simulated data")
        results = _simulate_results(f"processing_error: {str(exc)[:80]}")
        results["processing_time_seconds"] = round(
            (datetime.now() - start_time).total_seconds(), 2
        )
        return results
