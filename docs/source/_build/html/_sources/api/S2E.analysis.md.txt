# S2E.analysis — Embedding & Pattern Analysis

> **Module:** `S2E.analysis` | **Import:** `from S2E import analysis`

## Embedding Extraction

### `get_embedding(img_path_list, model_path, ...) -> np.ndarray`

*Source docstring* — Extract embeddings from a list of images using a trained vision model.

```python
def get_embedding(
    img_path_list: list[str],
    model_path: str,
    hf_model_name: Literal['google/vit-base-patch16-224', 'microsoft/swinv2-base-patch4-window16-256'] = 'microsoft/swinv2-base-patch4-window16-256',
    num_labels: int = 7,
    pooling: Literal['cls', 'mean'] = 'mean',
    batch_size: int = 64,
    num_workers: int = 4,
    verbose: bool = True,
) -> np.ndarray
```

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `img_path_list` | `list[str]` | *(required)* | List of image file paths. | Source docstring |
| `model_path` | `str` | *(required)* | Path to pretrained model weights. | Source docstring |
| `hf_model_name` | `Literal[...]` | `'microsoft/swinv2-base-patch4-window16-256'` | HuggingFace backbone. | Source docstring |
| `num_labels` | `int` | `7` | Output label count for model loading. | Source docstring |
| `pooling` | `'cls' \| 'mean'` | `'mean'` | Pooling strategy. | Source docstring |
| `batch_size` | `int` | `64` | Inference batch size. | Source docstring |
| `num_workers` | `int` | `4` | DataLoader workers. | Source docstring |
| `verbose` | `bool` | `True` | Show tqdm progress bar. | Source docstring |

| Returns | Type | Meaning |
|---------|------|---------|
| `embeddings` | `np.ndarray` | Shape `(N, embedding_dim)`. |

---

### `get_dataset_embeddings(img_root_path, model_path, ...) -> AnnData`

*Source docstring* — Extract embeddings from an ImageFolder-structured dataset directory.

```python
def get_dataset_embeddings(
    img_root_path: str,
    model_path: str,
    hf_model_name: ... = 'microsoft/swinv2-base-patch4-window16-256',
    num_labels: int = 7,
    pooling: Literal['cls', 'mean'] = 'mean',
    batch_size: int = 64,
    num_workers: int = 4,
    verbose: bool = True
) -> AnnData
```

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `img_root_path` | `str` | *(required)* | Directory with subfolders per gene (ImageFolder format). |
| `model_path` | `str` | *(required)* | Path to pretrained weights. |
| *(other)* | *(same as get_embedding)* | | |

| Returns | Type | Meaning |
|---------|------|---------|
| `adata` | `AnnData` | `.X`: embeddings `(N, D)`, `.obs`: `['cell', 'feature_name']`, `.var`: `['embedding']`. |

---

### `get_blank_pseudocell_embedding(model_path, ...) -> np.ndarray`

*Source docstring* — Generate a blank pseudo-cell image and extract its embedding as a reference/background.

```python
def get_blank_pseudocell_embedding(
    model_path: str,
    hf_model_name: ... = 'microsoft/swinv2-base-patch4-window16-256',
    num_labels: int = 7,
    pooling: Literal['cls', 'mean'] = 'mean',
    img_path: str = './blank_image.png',
    pseudo_cell_boundaries_radius: float = 2.783,
    dpi: int = 200
) -> np.ndarray
```

| Returns | Type | Meaning |
|---------|------|---------|
| `embedding` | `np.ndarray` | Shape `(embedding_dim,)` — the "empty" reference. |

---

## Pattern Prediction

### `pattern_predict(img_path_list, pretrained_model_path, ...) -> pd.DataFrame`

*Source docstring* — Predict relative pattern proportions (softmax over 7 patterns) for a list of images.

```python
def pattern_predict(
    img_path_list: list[str],
    pretrained_model_path: str,
    hf_model_name: ... = 'microsoft/swinv2-base-patch4-window16-256',
    num_labels: int = 7,
    pooling: Literal['cls', 'mean'] = 'mean',
    batch_size: int = 64,
    num_workers: int = 4,
    verbose: bool = True
) -> pd.DataFrame
```

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `img_path_list` | `list[str]` | *(required)* | Image file paths. |
| `pretrained_model_path` | `str` | *(required)* | Path to S2E pretrained weights. |

| Returns | Type | Meaning |
|---------|------|---------|
| `df` | `pd.DataFrame` | Columns: `['Intranuclear', 'Nuclear edge', 'Perinuclear', 'Extranuclear', 'Cell edge', 'Pericellular', 'Foci', 'img_path']`. Each row sums to 1. |

---

### `pattern_predict_for_dataset(img_root_path, pretrained_model_path, ...) -> AnnData`

*Source docstring* — Predict patterns for all images in a dataset directory.

| Returns | Type | Meaning |
|---------|------|---------|
| `adata` | `AnnData` | `.X`: `(N, 7)` softmax proportions, `.obs`: `['cell', 'feature_name']`, `.var`: `['pattern']`. |

---

## Data Classes

### `class EmbeddingAnndata`

*Source docstring* — Wrapper around `AnnData` for managing embedding data with dataset source labels.

```python
class EmbeddingAnndata:
    def __init__(self, adata: AnnData, dataset_name: str | list[str])
```

| Parameter | Type | Meaning | Source |
|-----------|------|---------|--------|
| `adata` | `AnnData` | Must have `.obs` with `'cell'` or `'feature_name'`; `.var` with `'embedding'`. | Source docstring |
| `dataset_name` | `str \| list[str]` | Dataset label(s). Single string or per-observation list. | Source docstring |

#### Methods

| Method | Signature | Meaning |
|--------|-----------|---------|
| `copy()` | `-> EmbeddingAnndata` | Deep copy. |
| `__add__(other)` | `-> EmbeddingAnndata` | Concatenate two instances (aligns variables, stacks observations). |
| `extract_embedding(cell=None, feature_name=None, dataset_name=None)` | `-> EmbeddingAnndata` | Filter by cell, gene, or dataset criteria. |

### `class ImageDataset(Dataset)`

*Inferred* — PyTorch Dataset for loading images from a flat list of file paths.

### `class CustomImageFolder(ImageFolder)`

*Inferred* — PyTorch ImageFolder variant that also returns `cell_id` (filename stem) alongside image and label.

---

## Visualization

### `draw_cell_gene(gene_data=None, cell_boundary=None, nuclei_boundary=None, ...) -> None`

*Source docstring* — Visualize gene positions overlaid on cell and nuclei membranes.

```python
def draw_cell_gene(
    gene_data: pd.DataFrame | None = None,
    cell_boundary: Polygon | None = None,
    nuclei_boundary: Polygon | None = None,
    gene_color: str | dict = 'red',
    gene_size: float = 5,
    membrane_color: str = 'black',
    membrane_linewidth: float = 2.5,
    axis_off: bool = True,
    img_title: str | None = None,
    legend: bool = False,
    legend_bbox_to_anchor: tuple = (1.15, 1),
    show_img: bool = True,
    save_img: bool = False,
    dpi: int = 200,
    img_path: str = './cell_gene_image.png',
    verbose: bool = True
) -> None
```

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `gene_data` | `pd.DataFrame \| None` | `None` | Must have `x`, `y`, `feature_name` columns. None = no genes plotted. |
| `cell_boundary` | `Polygon \| None` | `None` | Cell membrane. |
| `nuclei_boundary` | `Polygon \| None` | `None` | Nuclei membrane. |
| `gene_color` | `str \| dict` | `'red'` | Single color or `{gene: color}` mapping. |
| `gene_size` | `float` | `5` | Scatter point size. |
| `membrane_color` | `str` | `'black'` | Membrane line color. |
| `membrane_linewidth` | `float` | `2.5` | Membrane line width. |
| `axis_off` | `bool` | `True` | Hide axes. |
| `img_title` | `str \| None` | `None` | Plot title. |
| `legend` | `bool` | `False` | Show gene color legend. |
| `save_img` | `bool` | `False` | Save to file. |
| `dpi` | `int` | `200` | Output resolution. |
| `img_path` | `str` | `'./cell_gene_image.png'` | Save path. |

---

### `plot_pca_heatmap(gene_level_pca, ...) -> tuple | None`

*Source docstring* — Plot a clean heatmap of gene-level PCA loadings with optional hierarchical clustering.

```python
def plot_pca_heatmap(
    gene_level_pca: pd.DataFrame,
    cluster_rows: bool = True,
    cmap: str = "RdBu_r",
    vmin: float | None = None,
    vmax: float | None = None,
    figsize: tuple = (6, 8),
    ...
    return_plot: bool = False
) -> tuple | None
```

| Key Parameter | Type | Default | Meaning |
|---------------|------|---------|---------|
| `gene_level_pca` | `pd.DataFrame` | *(required)* | Rows = genes, columns = PCs. |
| `cluster_rows` | `bool` | `True` | Hierarchical clustering on rows. |
| `cmap` | `str` | `'RdBu_r'` | Colormap. |
| `cmap_center_symmetric` | `bool` | `True` | Center colormap at 0. |
| `save_fig` | `bool` | `False` | Save to file. |
| `return_plot` | `bool` | `False` | If True, returns `(fig, ax, df_reordered)`. |

---

### `plot_umap_from_adata(adata, color_by='feature_name', ..., leiden=False, ...) -> tuple | None`

*Source docstring* — Plot UMAP from AnnData with precomputed `obsm['X_umap']`. Optional Leiden clustering.

```python
def plot_umap_from_adata(
    adata: AnnData,
    color_by: str = "feature_name",
    size: float = 20.0,
    legend_loc: str = "right margin",
    legend_fontsize: float | None = 10,
    title: str = "UMAP",
    leiden: bool = False,
    leiden_key: str = "leiden",
    leiden_resolution: float = 1.0,
    compute_neighbors_if_missing: bool = True,
    use_rep: str = "X_pca",
    n_neighbors: int = 15,
    random_state: int | None = None,
    figsize: tuple = (6, 6),
    save_fig: bool = False,
    fig_path: str = "umap.png",
    dpi: int = 300,
    show: bool = False,
    return_plot: bool = False
) -> tuple | None
```

| Key Parameter | Type | Default | Meaning |
|---------------|------|---------|---------|
| `adata` | `AnnData` | *(required)* | Must have `obsm['X_umap']`. |
| `color_by` | `str` | `'feature_name'` | Column in `adata.obs` for coloring. |
| `leiden` | `bool` | `False` | Compute/show Leiden clusters. |
| `leiden_resolution` | `float` | `1.0` | Leiden resolution parameter. |
| `save_fig` | `bool` | `False` | Save to file. |
| `return_plot` | `bool` | `False` | Return figure/axes objects. |
