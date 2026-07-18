# S2E.processing — Data Processing

> **Module:** `S2E.processing` | **Import:** `from S2E import processing`

## `process_spatialdata_for_s2e(cell_boundaries, nuclei_boundaries, points_df, ...) -> sd.SpatialData`

*Source docstring* — Convert subcellular spatial transcriptomics data into an S2E-compatible SpatialData object. Performs polygon cleaning, cell-nucleus matching via overlap, rasterization, and transcript assignment.

```python
def process_spatialdata_for_s2e(
    cell_boundaries: GeoSeries | GeoDataFrame,
    nuclei_boundaries: GeoSeries | GeoDataFrame,
    points_df: pd.DataFrame,
    overlap_threshold: float = 0.2,
    coord_offset: int = 1,
    num_processes: int = 4,
    verbose: bool = False,
) -> sd.SpatialData
```

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `cell_boundaries` | `GeoSeries \| GeoDataFrame` | *(required)* | Cell membrane polygons. | Source docstring |
| `nuclei_boundaries` | `GeoSeries \| GeoDataFrame` | *(required)* | Nuclear membrane polygons. | Source docstring |
| `points_df` | `pd.DataFrame` | *(required)* | Transcript data with columns: `x`, `y`, `feature_name`. | Source docstring |
| `overlap_threshold` | `float` | `0.2` | Minimum cell-nucleus overlap ratio for assignment. | Source docstring |
| `coord_offset` | `int` | `1` | Pixel offset for raster mask lookup. | Source docstring |
| `num_processes` | `int` | `4` | Parallel workers for cell-nucleus matching. | Source docstring |
| `verbose` | `bool` | `False` | Print progress messages. | Source docstring |

| Returns | Type | Meaning |
|---------|------|---------|
| `sdata_out` | `sd.SpatialData` | SpatialData with `shapes['cell_boundaries']`, `shapes['nuclei_boundaries']`, `tables['table']`, and rasterized labels. |

---

## `normalize(data, pseudo_cell_boundaries_radius=2.783, ..., num_processes=2, copy=False) -> SubCE | None`

*Source docstring* — Normalize gene expression data to pseudo-cell space. Each cell's transcripts are radially projected based on their position between nuclear and cell membranes.

```python
def normalize(
    data: SubCE,
    pseudo_cell_boundaries_radius: float = 2.783,
    pts_key: str = 'points',
    cell_boundaries_key: str = 'cell_boundaries',
    nuclei_boundaries_key: str = 'nuclei_boundaries',
    num_processes: int = 2,
    copy: bool = False
) -> SubCE | None
```

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `data` | `SubCE` | *(required)* | SubCE with initialized `'raw'` layer. | Source docstring |
| `pseudo_cell_boundaries_radius` | `float` | `2.783` | Pseudo-cell membrane radius. | Source docstring |
| `pts_key` | `str` | `'points'` | Key for gene data in raw layer. | Source docstring |
| `cell_boundaries_key` | `str` | `'cell_boundaries'` | Key for cell membrane. | Source docstring |
| `nuclei_boundaries_key` | `str` | `'nuclei_boundaries'` | Key for nuclei membrane. | Source docstring |
| `num_processes` | `int` | `2` | Parallel processes. | Source docstring |
| `copy` | `bool` | `False` | Return modified copy instead of in-place. | Source docstring |

*Inferred* — Nuclear transcripts are normalized: `r_new = r / (r + d_membrane)`, meaning they stay within [0,1] (inside the nuclear membrane). Cytoplasmic transcripts: `r_new = 1 + (R-1) * d_nuc / (d_nuc + d_cell)`, placing them in [1, 2.783]. The normalization is parallelized via multiprocessing.

---

## `normalize_one_cell(gene_data, cell_membrane, nuclei_membrane, pseudo_cell_boundaries_radius=2.783) -> pd.DataFrame`

*Source docstring* — Normalize data for a single cell. Internal helper, parallelized by `normalize()`.

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `gene_data` | `pd.DataFrame` | *(required)* | Single-cell gene data with `x`, `y`, `cell`, `feature_name`, `nuclei`. |
| `cell_membrane` | `Polygon` | *(required)* | Cell membrane polygon. |
| `nuclei_membrane` | `Polygon` | *(required)* | Nuclei membrane polygon. |
| `pseudo_cell_boundaries_radius` | `float` | `2.783` | Target cell radius. |

| Returns | Type | Meaning |
|---------|------|---------|
| `normalized_data` | `pd.DataFrame` | Normalized coordinates `[x, y, cell, feature_name, nuclei]`. |

---

## `reconstruct(data, pts_key='points', ..., model_root_path='./ot_models', num_processes=2, copy=False) -> SubCE | None`

*Source docstring* — Reconstruct normalized gene expression points back to native cell morphology using per-cell Optimal Transport models.

```python
def reconstruct(
    data: SubCE,
    pts_key: str = 'points',
    cell_boundaries_key: str = 'cell_boundaries',
    nuclei_boundaries_key: str = 'nuclei_boundaries',
    model_root_path: str = './ot_models',
    num_processes: int = 2,
    copy: bool = False
) -> SubCE | None
```

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `data` | `SubCE` | *(required)* | SubCE with initialized `'raw'` and `'normalized'` layers. |
| `pts_key` | `str` | `'points'` | Key for gene data. |
| `cell_boundaries_key` | `str` | `'cell_boundaries'` | Key for cell membrane. |
| `nuclei_boundaries_key` | `str` | `'nuclei_boundaries'` | Key for nuclei membrane. |
| `model_root_path` | `str` | `'./ot_models'` | Directory with trained OT models (per cell: `{cell_id}_cyto.pkl`, `{cell_id}_nuclei.pkl`). |
| `num_processes` | `int` | `2` | Parallel processes. |
| `copy` | `bool` | `False` | Return copy if True. |

---

## `reconstruct_one_cell(gene_data, gene_name, cell_boundary, cell_id, model_root_path='./ot_models') -> pd.DataFrame`

*Source docstring* — Reconstruct normalized points for one cell using trained OT models. Points falling outside the cell membrane are filtered out.

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `gene_data` | `pd.DataFrame` | *(required)* | Normalized gene data for one cell. |
| `gene_name` | `str \| list[str] \| None` | *(required)* | Gene(s) to reconstruct. None = all. |
| `cell_boundary` | `Polygon` | *(required)* | Raw cell membrane polygon. |
| `cell_id` | `int \| str` | *(required)* | Cell ID for loading OT model. |
| `model_root_path` | `str` | `'./ot_models'` | OT model directory. |

---

## `generate_image_data(data, layer, pts_key, ..., dpi=200, num_processes=2) -> None`

*Source docstring* — Generate PNG images visualizing gene expression on cell membranes for all cell-gene instances.

```python
def generate_image_data(
    data: SubCE,
    layer: str,
    pts_key: str,
    cell_boundaries_key: str = 'cell_boundaries',
    nuclei_boundaries_key: str = 'nuclei_boundaries',
    save_root_path: str = './images_data',
    train_split_ratio: float | None = None,
    gene_color: str = 'red',
    gene_size: float = 5,
    membrane_color: str = 'black',
    membrane_linewidth: float = 2.5,
    dpi: int = 200,
    num_processes: int = 2,
) -> None
```

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `data` | `SubCE` | *(required)* | SubCE with gene expression data. | Source docstring |
| `layer` | `str` | *(required)* | Layer to visualize (`'raw'`, `'normalized'`, `'recon'`). | Source docstring |
| `pts_key` | `str` | *(required)* | Key for gene data in `data[layer].uns`. | Source docstring |
| `cell_boundaries_key` | `str` | `'cell_boundaries'` | Key for cell membrane. | Source docstring |
| `nuclei_boundaries_key` | `str` | `'nuclei_boundaries'` | Key for nuclei membrane. | Source docstring |
| `save_root_path` | `str` | `'./images_data'` | Root output directory. | Source docstring |
| `train_split_ratio` | `float \| None` | `None` | If set (e.g. 0.8), split into train/val subdirs. | Source docstring |
| `gene_color` | `str` | `'red'` | Color for gene markers. | Source docstring |
| `gene_size` | `float` | `5` | Scatter point size. | Source docstring |
| `membrane_color` | `str` | `'black'` | Membrane outline color. | Source docstring |
| `membrane_linewidth` | `float` | `2.5` | Membrane line width. | Source docstring |
| `dpi` | `int` | `200` | Output image resolution. | Source docstring |
| `num_processes` | `int` | `2` | Parallel processes. | Source docstring |

*Inferred* — Images are saved as `{save_root_path}/{gene_name}/{cell_id}.png` (or in `train/`/`val/` subdirs when split). Empty cell-gene instances are skipped.
