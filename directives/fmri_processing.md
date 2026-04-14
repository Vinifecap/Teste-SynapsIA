# Diretiva: Processamento fMRI — SynapsIA

## Objetivo
Processar arquivos NIfTI (.nii, .nii.gz) de fMRI para gerar pré-relatórios neurológicos
automatizados com mapas cerebrais visuais e análise de conectividade funcional.

## Inputs
- Arquivo fMRI: `.nii` ou `.nii.gz` (NIfTI 4D — dimensões: x, y, z, t)
- `output_dir`: pasta onde salvar imagens e JSON (`temp_uploads/{exam_id}/`)

## Ferramentas/Scripts
1. `execution/processing/fmri_pipeline.py` — Pipeline determinístico de processamento
2. `execution/processing/report_generator.py` — Gerador de imagens e PDF

## Passos do Pipeline

### 1. Validação do Arquivo
- Carregar com `nibabel.load()`
- Verificar shape 4D (x, y, z, t)
- Verificar mínimo de 10 volumes temporais
- Se inválido → retornar dados simulados realistas

### 2. Pré-processamento
```python
# Smoothing espacial (FWHM=6mm — padrão fMRI)
smoothed = nilearn.image.smooth_img(img, fwhm=6)

# Mascaramento cerebral com remoção de tendência e filtro passa-banda
masker = NiftiMasker(standardize=True, detrend=True,
                     low_pass=0.1, high_pass=0.01, t_r=2.0)
signals = masker.fit_transform(smoothed)
```

### 3. Extração de Conectividade
```python
# Parcelas usando atlas Schaefer 2018 (20 ROIs)
atlas = datasets.fetch_atlas_schaefer_2018(n_rois=20)
label_masker = NiftiLabelsMasker(labels_img=atlas.maps, standardize=True)
region_signals = label_masker.fit_transform(smoothed)

# Matriz de correlação de Pearson entre regiões
conn_measure = ConnectivityMeasure(kind="correlation")
conn_matrix = conn_measure.fit_transform([region_signals])[0]
```

### 4. Detecção de Anomalias
```python
# Z-score vs. baseline populacional (mean=0.35, std=0.12 — resting-state típico)
region_mean_conn = np.mean(np.abs(conn_matrix), axis=1)
z_scores = (region_mean_conn - 0.35) / 0.12
affected = np.where(np.abs(z_scores) > 2.0)[0]
```

### 5. Geração de Imagens
- Glass brain: `nilearn.plotting.plot_glass_brain()`
- Cortes axial/coronal/sagital: `nilearn.plotting.plot_anat()`
- Heatmap de conectividade: `matplotlib.pyplot.imshow()`
- Gráfico de z-scores: `matplotlib.pyplot.barh()`

### 6. Geração de PDF
- Biblioteca: `reportlab`
- Tema: escuro (#0a0a0f) com acentos azul (#4f8ef7) e roxo (#a855f7)
- Conteúdo: header, disclaimer, tabela de metadados, score, regiões, imagens, recomendações

## Outputs
```json
{
  "exam_id":                  "uuid",
  "exam_date":                "DD/MM/YYYY HH:MM",
  "processing_time_seconds":  float,
  "is_simulated":             bool,
  "n_volumes":                int,
  "n_regions_analyzed":       int,
  "mean_connectivity":        float,
  "affected_regions": [
    { "name": str, "z_score": float, "deviation": "alta|moderada", "laterality": str }
  ],
  "anomaly_score":   float,  // 0.0 a 1.0
  "anomaly_level":   "Baixo|Moderado|Alto",
  "recommendations": [str],
  "images": {
    "glass_brain": "/uploads/{id}/images/glass_brain.png",
    "axial":       "/uploads/{id}/images/axial.png",
    ...
  },
  "disclaimer":  str
}
```

## Fallback (Modo Simulado)
Ativado quando:
- Arquivo não é NIfTI 4D válido
- Shape tem < 10 volumes temporais
- nilearn não instalado
- Qualquer exceção durante o processamento

Retorna dados realistas com `"is_simulated": true` — permite demonstração sem arquivo real.

## Casos de Borda
- **Arquivo .nii.gz corrompido**: nibabel lança exceção → fallback simulado ativado
- **fMRI com TR diferente de 2s**: substituir `t_r=2.0` pelo valor real do header
- **Atlas Schaefer indisponível (sem internet)**: fallback para parcelas uniformes do sinal bruto
- **matplotlib no servidor Windows**: usar `matplotlib.use("Agg")` antes de importar pyplot
- **Arquivos grandes (>500MB)**: processamento pode levar 3-5 min; timeout de polling no frontend é 120s por padrão

## Aprendizados
- `matplotlib.use("Agg")` DEVE ser chamado antes de qualquer import do pyplot em ambiente servidor
- nilearn precisa de `memory_level=0` no NiftiMasker para evitar cache em disco no MVP
- A detecção de anomalias usa baseline simulado (mean=0.35, std=0.12) — substituir por valores de banco normativo real em produção
