# S2E — Core Data Structure

> **Module:** `S2E._core.subcellular_embedding` | **Import:** `from S2E import SubCE`

## `class SubCE`

```python
class SubCE:
    def __init__(
        self,
        gene_data: pd.DataFrame,
        cell_boundaries: GeoSeries,
        nuclei_boundaries: GeoSeries,
        pts_key: str = 'points',
        cell_boundaries_key: str = 'cell_boundaries',
        nuclei_boundaries_key: str = 'nuclei_boundaries'
    ) -> None
```

*Source docstring* — The SubCE class stores and manipulates subcellular gene expression data across three layers (AnnData objects): `'raw'`, `'normalized'`, and `'recon'`.

### Constructor Parameters

| Name | Type | Default | Meaning | Source |
|------|------|---------|---------|--------|
| `gene_data` | `pd.DataFrame` | *(required)* | Transcript-level gene data with columns: `x`, `y`, `cell`, `feature_name`. Optional `nuclei` column (auto-computed if missing). | Source docstring |
| `cell_boundaries` | `geopandas.GeoSeries` | *(required)* | Cell membrane polygons indexed by cell ID. | Source docstring |
| `nuclei_boundaries` | `geopandas.GeoSeries` | *(required)* | Nuclei membrane polygons indexed by cell ID. | Source docstring |
| `pts_key` | `str` | `'points'` | Key for storing transcript data in `adata.uns`. | Source docstring |
| `cell_boundaries_key` | `str` | `'cell_boundaries'` | Key for cell membrane storage. | Source docstring |
| `nuclei_boundaries_key` | `str` | `'nuclei_boundaries'` | Key for nuclei membrane storage. | Source docstring |

### Class Attributes

| Name | Type | Meaning | Source |
|------|------|---------|--------|
| `X` | `np.ndarray` | Raw single-cell expression matrix (cells × genes). | Source docstring |
| `cell` | `list[int\|str]` | Cell names in row order of X. | Source docstring |
| `gene` | `list[str]` | Gene names in column order of X. | Source docstring |
| `layer` | `dict[str, AnnData]` | Three layers: `'raw'`, `'normalized'`, `'recon'`. Access via `se[layer_name]` or `se.layer[layer_name]`. | Source docstring |
| `pseudo_cell_boundaries_radius` | `float \| None` | Pseudo-cell membrane radius; `None` if normalized layer not initialized. | Source docstring |

### Instance Methods

#### `__getitem__(keys: str | list[str]) -> AnnData | dict[str, AnnData]`

*Source docstring* — Get AnnData object(s) from specified layer(s). Raises `KeyError` for unknown layers, `ValueError` for uninitialized layers, `TypeError` for invalid key types.

| Parameter | Type | Meaning |
|-----------|------|---------|
| `keys` | `str \| list[str]` | Layer name(s) to retrieve. |

| Returns | Type | Meaning |
|---------|------|---------|
| *(result)* | `AnnData \| dict[str, AnnData]` | Single layer or dict of layers. |

#### `__setitem__(keys: str | list[str], value: AnnData | dict[str, AnnData]) -> None`

*Inferred* — Set AnnData object(s) for specified layer(s). Validates key existence and type consistency.

#### `layer_init(layer, gene_data, cell_boundaries, nuclei_boundaries, pts_key='points', cell_boundaries_key='cell_boundaries', nuclei_boundaries_key='nuclei_boundaries', pseudo_cell_boundaries_radius=2.783) -> None`

*Source docstring* — Initialize a specified layer with gene expression data and membrane geometries. For the `'raw'` layer, nuclei centers are automatically translated to the origin. For `'normalized'`, the pseudo-cell radius is recorded.

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `layer` | `str` | *(required)* | Must be `'raw'`, `'normalized'`, or `'recon'`. |
| `gene_data` | `pd.DataFrame` | *(required)* | Transcript-level gene expression data. |
| `cell_boundaries` | `GeoSeries` | *(required)* | Cell membrane polygons. |
| `nuclei_boundaries` | `GeoSeries` | *(required)* | Nuclei membrane polygons. |
| `pts_key` | `str` | `'points'` | Key for points storage. |
| `cell_boundaries_key` | `str` | `'cell_boundaries'` | Key for cell boundaries storage. |
| `nuclei_boundaries_key` | `str` | `'nuclei_boundaries'` | Key for nuclei boundaries storage. |
| `pseudo_cell_boundaries_radius` | `float` | `2.783` | Pseudo-cell membrane radius (normalized layer only). |

#### `copy() -> SubCE`

*Source docstring* — Create a deep copy of the SubCE object via `copy.deepcopy`.

#### `move_nuclei_center_to_origin(gene_data, cell_boundaries, nuclei_boundaries) -> tuple[pd.DataFrame, GeoSeries, GeoSeries]` *(static)*

*Source docstring* — Translate all coordinates so that each cell's nucleus center is at the origin. Operates per-cell: subtracts the nucleus centroid from transcripts, cell membrane, and nucleus membrane.

| Parameter | Type | Meaning |
|-----------|------|---------|
| `gene_data` | `pd.DataFrame` | Input gene expression data. |
| `cell_boundaries` | `GeoSeries` | Cell membrane polygons. |
| `nuclei_boundaries` | `GeoSeries` | Nuclei membrane polygons. |

| Returns | Type | Meaning |
|---------|------|---------|
| `new_gene_data` | `pd.DataFrame` | Updated gene data with centered coordinates. |
| `new_cell_boundaries` | `GeoSeries` | Translated cell membrane polygons. |
| `new_nuclei_boundaries` | `GeoSeries` | Translated nuclei membrane polygons. |

### Usage Example

```python
from S2E import SubCE
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

gene_data = pd.DataFrame([
    [0, 0, 1, 'RPS3', 1],
    [1.5, 1.5, 1, 'RPS3', 0],
], columns=['x', 'y', 'cell', 'feature_name', 'nuclei'])

cell_boundaries = gpd.GeoSeries(
    Polygon([(-3, -3), (-3, 3), (3, 3), (3, -3)]),
    index=[1]
)
nuclei_boundaries = gpd.GeoSeries(
    Polygon([(-1, -1), (-1, 1), (1, 1), (1, -1)]),
    index=[1]
)

se = SubCE(gene_data, cell_boundaries, nuclei_boundaries)
print(se.cell)   # [1]
print(se.gene)   # ['RPS3']
raw = se['raw']  # Access raw layer
```
