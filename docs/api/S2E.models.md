# S2E.models — Model Infrastructure

> **Module:** `S2E.models` | **Import:** `from S2E import models`

## `class HuggingFace_Model(nn.Module)`

*Source docstring* — Wrapper around HuggingFace ViT/SwinV2 models for classification or regression with configurable pooling.

```python
class HuggingFace_Model(nn.Module):
    def __init__(
        self,
        hf_model_name: Literal['google/vit-base-patch16-224', 'microsoft/swinv2-base-patch4-window16-256'] = 'microsoft/swinv2-base-patch4-window16-256',
        num_labels: int = 7,
        pooling: Literal['cls', 'mean'] = 'mean',
        output_pooled_last_hidden_state: bool = False,
        local_files_only: bool = False,
        cache_dir: str | None = None,
        pretrained_model_path: str | None = None
    )
```

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `hf_model_name` | `Literal[...]` | `'microsoft/swinv2-base-patch4-window16-256'` | HuggingFace backbone. SwinV2 only supports `'mean'` pooling. | Source docstring |
| `num_labels` | `int` | `7` | Output dimension (classes or targets). | Source docstring |
| `pooling` | `'cls' \| 'mean'` | `'mean'` | CLS token or mean of patch tokens. | Source docstring |
| `output_pooled_last_hidden_state` | `bool` | `False` | If True, also return the pooled embedding. | Source docstring |
| `local_files_only` | `bool` | `False` | Only load from local cache. | Source docstring |
| `cache_dir` | `str \| None` | `None` | HF cache directory. | Source docstring |
| `pretrained_model_path` | `str \| None` | `None` | External checkpoint path. If provided, loads backbone weights via `load_state_dict` with strict=False. | Source docstring |

### `forward(pixel_values: torch.Tensor) -> dict`

*Source docstring* — Forward pass returning `{'logits': tensor(B, num_labels)}` and optionally `{'embedding': tensor(B, hidden_dim)}` if `output_pooled_last_hidden_state=True`.

---

## `train_ot_model(cell_boundaries, nuclei_boundaries, cell_id=None, ...) -> None`

*Source docstring* — Train per-cell Optimal Transport models for cytoplasm and nucleus, enabling reconstruction from normalized to native space.

```python
def train_ot_model(
    cell_boundaries: GeoSeries,
    nuclei_boundaries: GeoSeries,
    cell_id: int | str | list | None = None,
    num_points: int = 1024,
    pseudo_cell_boundaries_radius: float = 2.783,
    num_processes: int = 4,
    cyto_ot_model_init: ot.da.MappingTransport | None = None,
    nuclei_ot_model_init: ot.da.MappingTransport | None = None,
    save_root_path: str = "./ot_models",
    draw_sample: int | str | None = None,
) -> None
```

| Parameter | Type | Default | Meaning | Source |
|-----------|------|---------|---------|--------|
| `cell_boundaries` | `GeoSeries` | *(required)* | Cell membrane polygons indexed by cell ID. | Source docstring |
| `nuclei_boundaries` | `GeoSeries` | *(required)* | Nucleus polygons. | Source docstring |
| `cell_id` | `int\|str\|list\|None` | `None` | Cell(s) to process. None = all. | Source docstring |
| `num_points` | `int` | `1024` | Sampling points per cell (cytoplasm + nucleus). | Source docstring |
| `pseudo_cell_boundaries_radius` | `float` | `2.783` | Pseudo-cell radius for normalization. | Source docstring |
| `num_processes` | `int` | `4` | Parallel workers. | Source docstring |
| `cyto_ot_model_init` | `MappingTransport \| None` | `None` | Custom cytoplasm OT model; defaults to `ot.da.MappingTransport(kernel='gaussian', eta=1e-5, mu=1e-1, max_iter=10)`. | Source docstring |
| `nuclei_ot_model_init` | `MappingTransport \| None` | `None` | Custom nucleus OT model. | Source docstring |
| `save_root_path` | `str` | `'./ot_models'` | Output directory for `{cell_id}_cyto.pkl` / `{cell_id}_nuclei.pkl`. | Source docstring |
| `draw_sample` | `int\|str\|None` | `None` | If set to a cell ID, saves diagnostic plots (raw/normalized/recon) for that cell. | Source docstring |

*Inferred* — The OT training samples points uniformly inside each cell (proportional to nucleus/cytoplasm area), normalizes them to pseudo-cell space, then fits `MappingTransport` models mapping pseudo-cell → native coordinates.

> **Note:** NumPy ≥2.0 is recommended for faster training due to improved numerical routines.

---

## Model Utilities (`_model_utils.py`, `_cached.py`)

Internal helper functions (prefixed with underscore) used by embedding and pattern modules:

| Function | Purpose | Source |
|----------|---------|--------|
| `_load_model_and_processor(hf_model_name, num_labels, pooling, ...)` | Load HuggingFace model + image processor with cache handling. | Inferred |
| `_build_transforms(processor)` | Build train/val image transforms from the processor. | Inferred |
| `_get_amp_helpers()` | Return autocast context manager for mixed-precision inference. | Inferred |
| `_is_model_cached(hf_model_name)` | Check if model is available in local cache. | Inferred |

---

## Trainer Module (`trainer.py`)

*Inferred* — Provides training utilities for fine-tuning the ViT/SwinV2 backbone on custom classification tasks. Not covered in detail here as it is primarily used internally for pre-training.

### Usage Example

```python
from S2E.models import train_ot_model, HuggingFace_Model
import geopandas as gpd

# Train OT models
train_ot_model(
    cell_boundaries=se['raw'].uns['cell_boundaries'],
    nuclei_boundaries=se['raw'].uns['nuclei_boundaries'],
    num_points=1024,
    num_processes=4,
    save_root_path='./ot_models'
)

# Load the S2E vision model
model = HuggingFace_Model(
    hf_model_name='microsoft/swinv2-base-patch4-window16-256',
    num_labels=7,
    pooling='mean',
    output_pooled_last_hidden_state=True,
    pretrained_model_path='./S2E-pattern-model/pytorch_model.bin'
)
```
