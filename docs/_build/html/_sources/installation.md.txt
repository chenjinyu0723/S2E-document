# Installation

## Prerequisites

- **Python**: >= 3.10
- **CUDA-capable GPU** recommended for embedding extraction and pattern prediction (CPU fallback supported)
- **Pretrained model weights** from [HuggingFace](https://huggingface.co/hinatakaho/S2E-pattern-model)

## Installing from Source

```bash
# Clone the repository
git clone <repository-url>
cd S2E

# Install in editable mode
pip install -e .
```

## Dependencies

S2E v0.1.2 requires the following packages (managed automatically by pip install):

| Package | Version | Purpose |
|---------|---------|---------|
| `pyarrow` | ≤20.0.0 | Data serialization |
| `spatial-image` | ≤1.2.1 | Spatial image handling |
| `multiscale-spatial-image` | ≤2.0.2 | Multi-scale images |
| `spatialdata` | ≤0.4.0 | Spatial omics data container |
| `POT` | ≤0.9.5 | Optimal transport (Python OT) |
| `cajal` | ≤1.0.3 | GW distance for morphology |
| `scanpy[leiden]` | ≤1.11.0 | Single-cell analysis toolkit |
| `qc-procrustes` | ≤1.1.1 | Procrustes alignment |
| `rasterio` | ≤1.4.3 | Raster data processing |
| `igraph` | ≤0.11.9 | Graph algorithms |
| `h5py` | ≤3.15.1 | HDF5 file handling |
| `xarray-dataclasses` | ≤1.9.1 | Typed xarray structures |
| `setuptools` | ≤80.9.0 | Build system |

Additional runtime dependencies (installed automatically as transitive dependencies):
- `torch`, `torchvision` — PyTorch deep learning framework
- `transformers` — HuggingFace Transformers for ViT/SwinV2 models
- `geopandas`, `shapely` — Geometric operations
- `numpy`, `pandas`, `scipy`, `scikit-learn` — Scientific computing
- `matplotlib`, `seaborn` — Visualization
- `tqdm` — Progress bars
- `Pillow` — Image processing
- `tifffile` — TIFF I/O

## Verifying Installation

```python
import S2E
print(S2E.__version__)  # or check that SubCE is available
from S2E import SubCE
print("S2E installed successfully!")
```

## Pretrained Model Download

```bash
# Download from HuggingFace Hub
git lfs install
git clone https://huggingface.co/hinatakaho/S2E-pattern-model
```

The pretrained model path is then passed to embedding/pattern functions via the `model_path` or `pretrained_model_path` parameter.

## Building Documentation

```bash
cd docs
pip install -r requirements-docs.txt
sphinx-build -b html . _build/html
# Open _build/html/index.html in your browser
```
