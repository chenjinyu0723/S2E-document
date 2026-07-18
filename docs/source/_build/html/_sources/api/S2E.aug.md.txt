# S2E.aug — Augmentation

> **Module:** `S2E.aug` | **Import:** `from S2E import aug`

## `cell_gene_augmentation(data, pts_key='points', ..., k=19, ..., num_processes=4, copy=False) -> SubCE | None`

*Source docstring* — Augment gene point patterns for reference cells using auxiliary cells. This is the **metacell augmentation** step that dramatically increases effective transcript density.

```python
def cell_gene_augmentation(
    data: SubCE,
    pts_key: str = 'points',
    cell_boundaries_key: str = 'cell_boundaries',
    nuclei_boundaries_key: str = 'nuclei_boundaries',
    save_pts_key: str = 'augmented_points',
    gene_name: str | list[str] | None = None,
    k: int = 19,
    reference_auxiliary_cell_id_dict: dict | None = None,
    aug_method: Literal['raw_gene', 'closest_pattern'] = 'raw_gene',
    align_method: Literal['linear', 'rotate', None] = 'rotate',
    top_genes_num: int = 200,
    distance_metric: Literal['gw_dist', 'procrustes', 'hausdorff', 'wasserstein'] = 'gw_dist',
    closest_pattern_num: int = 10,
    unique_cells: bool = False,
    save_rotation_angle: bool = False,
    num_processes: int = 4,
    copy: bool = False
) -> SubCE | None
```

### Core Parameters

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `data` | `SubCE` | *(required)* | SubCE with initialized `'normalized'` layer. | Source docstring |
| `pts_key` | `str` | `'points'` | Key for normalized points. | Source docstring |
| `k` | `int` | `19` | Number of auxiliary cells per reference cell. | Source docstring |
| `save_pts_key` | `str` | `'augmented_points'` | Key for augmented output in `data['normalized'].uns`. | Source docstring |
| `gene_name` | `str \| list[str] \| None` | `None` | Genes to augment. None = all genes. | Source docstring |
| `aug_method` | `'raw_gene' \| 'closest_pattern'` | `'raw_gene'` | **Use `'raw_gene'`** — the `'closest_pattern'` method is experimental and performs poorly. | Source docstring |
| `align_method` | `'linear' \| 'rotate' \| None` | `'rotate'` | Alignment method. `'rotate'` is recommended; `'linear'` is experimental. | Source docstring |
| `num_processes` | `int` | `4` | Parallel workers. | Source docstring |
| `copy` | `bool` | `False` | Return modified copy if True. | Source docstring |

### Auxiliary Cell Mapping

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `reference_auxiliary_cell_id_dict` | `dict \| None` | `None` | Explicit `{ref_cell: [aux_cells...]}` mapping. Overrides random k-sampling. | Source docstring |

### Discouraged Parameters (closest_pattern only)

| Parameter | Type | Default | Note |
|-----------|------|---------|------|
| `top_genes_num` | `int` | `200` | Only for `'closest_pattern'`. Ignore in practice. |
| `distance_metric` | `str` | `'gw_dist'` | Only for `'closest_pattern'`. Ignore in practice. |
| `closest_pattern_num` | `int` | `10` | Only for `'closest_pattern'`. Ignore in practice. |
| `unique_cells` | `bool` | `False` | Only for `'closest_pattern'`. Ignore in practice. |

### Returns

If `copy=True`, returns SubCE with `data['normalized'].uns[save_pts_key]` containing augmented points with columns: `['x', 'y', 'cell', 'feature_name', 'source_auxiliary_cell', 'source_feature_name', 'nuclei']`.

---

## `build_reference_auxiliary_map(cells, step=20, drop_last=True) -> dict`

*Source docstring* — Build a mapping from reference cells to auxiliary cell lists based on input ordering. Groups cells into blocks of size `step`.

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `cells` | `list[int\|str]` | *(required)* | Ordered list of cell IDs. | Source docstring |
| `step` | `int` | `20` | Block size (reference + step-1 auxiliaries). Must be ≥2. | Source docstring |
| `drop_last` | `bool` | `True` | If True, drop incomplete last block; if False, pad by wrapping. | Source docstring |

| Returns | Type | Meaning |
|---------|------|---------|
| `mapping` | `dict` | `{ref_cell_id: [aux_cell_ids...]}` in input order. |

---

## `get_similar_cells_in_morphology(sdata=None, tiff_root_path=None, ...) -> dict[int, list[int]]`

*Source docstring* — Compute morphological similarity between segmented cells using Gromov-Wasserstein distances via the `cajal` pipeline.

```python
def get_similar_cells_in_morphology(
    sdata: SpatialData | None = None,
    tiff_root_path: str | None = None,
    out_path: str = './similar_cells.csv',
    tmp_root_path: str = './tmp_path',
    n_sample: int = 100,
    num_processes: int = 8,
    save_csv: bool = True,
    verbose: bool = True
) -> dict[int, list[int]]
```

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `sdata` | `SpatialData \| None` | `None` | SpatialData with `labels['cell_mask']`. Takes precedence over `tiff_root_path`. | Source docstring |
| `tiff_root_path` | `str \| None` | `None` | Folder with CellPose TIFF files. | Source docstring |
| `out_path` | `str` | `'./similar_cells.csv'` | CSV output path. | Source docstring |
| `n_sample` | `int` | `100` | Sample points per cell for ICDM. | Source docstring |
| `num_processes` | `int` | `8` | Parallel workers. | Source docstring |

| Returns | Type | Meaning |
|---------|------|---------|
| `neighbors_dict` | `dict` | `{cell_id: [neighbor_ids sorted by GW distance]}`. |

### Usage Example

```python
from S2E import aug

# Basic metacell augmentation
aug.cell_gene_augmentation(se, k=19, num_processes=4)

# With explicit auxiliary mapping
cell_map = aug.build_reference_auxiliary_map(se.cell, step=20)
aug.cell_gene_augmentation(se, k=19, reference_auxiliary_cell_id_dict=cell_map)

# Find morphologically similar cells
neighbors = aug.get_similar_cells_in_morphology(sdata=sdata, n_sample=100)
```
