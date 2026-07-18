# S2E.get — Data Extraction

> **Module:** `S2E.get.get_data` | **Import:** `from S2E.get import get_gene_data, get_membrane_polygon, get_normalized_membrane`

## `get_membrane_polygon(data, cell_id=None, cell_boundaries_key='cell_boundaries', nuclei_boundaries_key='nuclei_boundaries', return_polygon=False)`

*Source docstring* — Return cell and nuclei membrane geometries from AnnData or SpatialData.

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `data` | `SpatialData \| AnnData` | *(required)* | Input containing membrane boundary geometries. | Source docstring |
| `cell_id` | `int \| str \| ArrayLike \| None` | `None` | Cell ID(s) to extract. If None, return all. | Source docstring |
| `cell_boundaries_key` | `str` | `'cell_boundaries'` | Key for cell membrane GeoSeries/GeoDataFrame. | Source docstring |
| `nuclei_boundaries_key` | `str` | `'nuclei_boundaries'` | Key for nucleus membrane. | Source docstring |
| `return_polygon` | `bool` | `False` | If True and single cell_id, return Polygon instead of GeoSeries. | Source docstring |

| Returns | Type | Meaning |
|---------|------|---------|
| `cell_boundaries` | `GeoSeries \| Polygon` | Cell membrane geometries. |
| `nuclei_boundaries` | `GeoSeries \| Polygon` | Nucleus membrane geometries. |

*Inferred* — For SpatialData input, boundaries are extracted from `data.shapes[key]['geometry']`. For AnnData, from `data.uns[key]`.

---

## `get_gene_data(data, pts_key='points', cell_id=None, gene_name=None, exclude_cell_id=None, top_genes_by_expression=None, return_top_genes_list=False) -> pd.DataFrame | tuple`

*Source docstring* — Retrieve a transcript DataFrame from SpatialData or AnnData with optional filtering.

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `data` | `SpatialData \| AnnData` | *(required)* | Object containing transcript-level point data. | Source docstring |
| `pts_key` | `str` | `'points'` | Key for the transcript DataFrame. | Source docstring |
| `cell_id` | `int \| str \| ArrayLike \| None` | `None` | Filter to these cell IDs. | Source docstring |
| `gene_name` | `str \| ArrayLike \| None` | `None` | Filter to these gene names. | Source docstring |
| `exclude_cell_id` | `int \| str \| ArrayLike \| None` | `None` | Exclude these cell IDs. | Source docstring |
| `top_genes_by_expression` | `int \| None` | `None` | Select top-N most frequently observed genes. | Source docstring |
| `return_top_genes_list` | `bool` | `False` | If True with top_genes, also return the gene list. | Source docstring |

| Returns | Type | Meaning |
|---------|------|---------|
| `gene_data` | `pd.DataFrame` | Filtered transcript DataFrame with columns: `x`, `y`, `cell`, `feature_name`, `nuclei`. |
| `top_genes_list` | `list[str]` | *(optional)* Top-N gene names when `return_top_genes_list=True`. |

---

## `get_normalized_membrane(pseudo_cell_boundaries_radius=2.783) -> tuple[Polygon, Polygon]`

*Source docstring* — Generate pseudo-cell membrane polygons: a unit circle (radius=1) for the nucleus and a larger circle for the cell membrane.

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `pseudo_cell_boundaries_radius` | `float` | `2.783` | Radius of the pseudo-cell membrane. | Source docstring |

| Returns | Type | Meaning |
|---------|------|---------|
| `cell_boundaries` | `Polygon` | Circular cell membrane (360-point approximation). |
| `nuclei_boundaries` | `Polygon` | Circular nuclei membrane (radius=1, 360-point). |

*Inferred* — Both polygons are centered at (0, 0). Used as the standardized target geometry during normalization.

### Usage Example

```python
from S2E.get import get_gene_data, get_membrane_polygon, get_normalized_membrane

# Extract from SpatialData
gene_df = get_gene_data(sdata, top_genes_by_expression=500)
cell_bounds, nuc_bounds = get_membrane_polygon(sdata)

# Get standard pseudo-cell geometry
cell_membrane, nuclei_membrane = get_normalized_membrane(pseudo_cell_boundaries_radius=2.783)
```
