# S2E.utils — Utilities

> **Module:** `S2E.utils` | **Import:** `from S2E import utils`

## I/O Functions

### `save(data, file_path, verbose=False) -> None`

*Source docstring* — Save any pickleable Python object to disk.

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `data` | `Any` | *(required)* | Pickleable Python object. | Source docstring |
| `file_path` | `str` | *(required)* | Output path (`.pkl` recommended). | Source docstring |
| `verbose` | `bool` | `False` | Print confirmation message. | Source docstring |

---

### `load(file_path, verbose=False) -> Any`

*Source docstring* — Load a pickled Python object from disk.

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `file_path` | `str` | *(required)* | Pickle file path. |
| `verbose` | `bool` | `False` | Print confirmation. |

| Returns | Type | Meaning |
|---------|------|---------|
| `data` | `Any` | Deserialized Python object. |

---

### `save_to_spatialdata(data, prefix='SubCE', ...) -> SpatialData`

*Source docstring* — Convert a SubCE object into a SpatialData instance, preserving all layers and geometries.

```python
def save_to_spatialdata(
    data: SubCE,
    prefix: str = "SubCE",
    cell_boundaries_key: str = "cell_boundaries",
    nuclei_boundaries_key: str = "nuclei_boundaries"
) -> SpatialData
```

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `data` | `SubCE` | *(required)* | SubCE with at least `'raw'` layer initialized. |
| `prefix` | `str` | `'SubCE'` | Prefix for table/shape keys (e.g. `'SubCE_raw'`). |

| Returns | Type | Meaning |
|---------|------|---------|
| `sdata` | `SpatialData` | Contains tables (`SubCE_raw`, `SubCE_normalized`, `SubCE_recon`) and shapes (cell/nuclei boundaries per layer). |

---

### `load_from_spatialdata(sdata, prefix='SubCE', ...) -> SubCE`

*Source docstring* — Reconstruct a SubCE object from a SpatialData saved by `save_to_spatialdata`.

```python
def load_from_spatialdata(
    sdata: SpatialData,
    prefix: str = "SubCE",
    cell_boundaries_key: str = "cell_boundaries",
    nuclei_boundaries_key: str = "nuclei_boundaries",
) -> SubCE
```

| Returns | Type | Meaning |
|---------|------|---------|
| `se` | `SubCE` | Restored SubCE with all available layers. |

---

## Distance Metrics

### `cosine_dissimilarity(emb1, emb2) -> float`

*Source docstring* — Calculate cosine dissimilarity: `1 - cosine_similarity`. Range [0.0, 2.0].

| Parameter | Type | Meaning |
|-----------|------|---------|
| `emb1` | `np.ndarray` | First embedding vector. |
| `emb2` | `np.ndarray` | Second embedding vector. |

| Returns | Type | Meaning |
|---------|------|---------|
| `dissimilarity` | `float` | `1 - cos(θ)`. Returns `NaN` if either vector is zero. |

---

## Point-Polygon Operations (`pts_polygon_related.py`)

Internal geometry helpers:

| Function | Purpose | Source |
|----------|---------|--------|
| `calc_polygon_center(polygon)` | Calculate centroid of a Shapely polygon. | Inferred |
| `compute_nuclei_column(gene_data, nuclei_boundaries, num_processes)` | Determine which transcripts fall inside nuclei (sets `nuclei` column: 1=inside, 0=outside). | Inferred |
| `calc_distances_to_membrane(pts, polygon)` | Compute shortest distances from points to polygon boundary. | Inferred |
| `calc_distances_to_center(pts, center)` | Compute distances and unit vectors from points to a center point. | Inferred |
| `get_points_in_polygon(pts, polygon)` | Filter points to those inside a polygon (Shapely `contains`). | Inferred |
| `compute_pts_dist(pts1, pts2, distance_metric)` | Compute distance between two point clouds using specified metric (`gw_dist`, `procrustes`, `hausdorff`, `wasserstein`). | Inferred |

### Usage Example

```python
from S2E.utils import save, load, save_to_spatialdata, load_from_spatialdata, cosine_dissimilarity

# Save/Load SubCE via SpatialData
sdata = save_to_spatialdata(se, prefix="MyExperiment")
se_restored = load_from_spatialdata(sdata, prefix="MyExperiment")

# Compare embeddings
dist = cosine_dissimilarity(embedding_a, embedding_b)
print(f"Cosine distance: {dist:.4f}")
```
