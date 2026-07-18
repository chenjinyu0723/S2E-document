# Architecture

## Package Structure

```
S2E/
├── __init__.py          # Package entry, exports SubCE + subpackages
├── _core/
│   ├── __init__.py
│   └── subcellular_embedding.py  # SubCE: core data structure
├── get/
│   ├── __init__.py
│   └── get_data.py      # Data extraction from SpatialData/AnnData
├── processing/
│   ├── __init__.py
│   ├── format.py         # SpatialData preprocessing
│   ├── normalized.py     # Pseudo-cell normalization
│   ├── reconstruct.py    # OT-based reconstruction
│   └── image_process.py  # Image generation from points
├── aug/
│   ├── __init__.py
│   ├── aug_utils.py      # Auxiliary cell mapping
│   ├── cell_gene_aug.py  # Metacell augmentation
│   └── cajal.py          # Morphological similarity via GW distance
├── analysis/
│   ├── __init__.py
│   ├── embedding.py      # ViT embedding extraction
│   ├── pattern.py        # Pattern prediction
│   └── plot.py           # Visualization utilities
├── models/
│   ├── __init__.py
│   ├── hf_model.py       # HuggingFace ViT/SwinV2 wrapper
│   ├── ot_models.py      # Optimal Transport model training
│   ├── trainer.py        # Training loop utilities
│   ├── _model_utils.py   # Model loading & transform helpers
│   └── _cached.py        # Model cache management
└── utils/
    ├── __init__.py
    ├── io.py             # Serialization (pickle/SpatialData)
    ├── metrics.py        # Distance metrics
    └── pts_polygon_related.py  # Point-polygon operations
```

## Three-Layer Data Model

The core `SubCE` class maintains three AnnData layers:

```{mermaid}
flowchart LR
    accTitle: S2E Three-Layer Data Architecture
    accDescr: Raw transcript points flow through normalization to produce normalized pseudo-cell data, then through optimal transport reconstruction back to native cell morphology.

    raw["🔴 Raw Layer\nNative morphology\nTranscript coordinates\n+ cell/nuclei polygons"]
    norm["🟡 Normalized Layer\nPseudo-cell space\nnucleus radius=1\ncell radius=2.783"]
    recon["🟢 Recon Layer\nNative morphology\nOT-reconstructed\nfrom normalized"]

    raw -->|"normalize()"| norm
    norm -->|"reconstruct()"| recon

    classDef raw fill:#fee2e2,stroke:#dc2626,color:#991b1b
    classDef norm fill:#fef9c3,stroke:#ca8a04,color:#713f12
    classDef recon fill:#dcfce7,stroke:#16a34a,color:#14532d

    class raw raw
    class norm norm
    class recon recon
```

### Raw Layer
Stores original single-molecule transcript coordinates and membrane polygons. Nuclei centers are translated to the origin via `move_nuclei_center_to_origin()`.

### Normalized Layer
Transcripts are projected into a standardized pseudo-cell coordinate system. Nuclear transcripts map to [0,1] radius; cytoplasmic transcripts map to [1, 2.783] radius based on their relative position between the nuclear and cell membranes.

### Recon Layer
Augmented metacell transcripts are mapped back to native cell morphology using per-cell Optimal Transport models, enabling visualization and analysis in original cell coordinates.

## Pipeline Flow

```{mermaid}
flowchart TD
    accTitle: S2E Complete Analysis Pipeline
    accDescr: Data flows from spatial omics input through preprocessing, normalization, metacell augmentation, image rendering, ViT embedding, and downstream analysis.

    A["📊 Spatial Omics Data\n(points + polygons)"] --> B["🔄 process_spatialdata_for_s2e()\nFormat & match cells/nuclei"]
    B --> C["📦 SubCE(data, cell_bounds, nuc_bounds)\nInitialize raw layer"]
    C --> D["📐 normalize()\nProject to pseudo-cell space"]
    D --> E["📈 cell_gene_augmentation()\nMetacell augmentation (k cells)"]
    E --> F["🖼️ generate_image_data()\nRender cell-gene images"]
    F --> G["🧠 get_dataset_embeddings()\nViT/SwinV2 embedding extraction"]
    G --> H["📉 PCA / UMAP / Clustering\nDownstream analysis"]
    G --> I["🏷️ pattern_predict()\nPattern classification"]

    classDef input fill:#dbeafe,stroke:#2563eb,color:#1e3a5f
    classDef process fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef output fill:#d1fae5,stroke:#059669,color:#064e3b

    class A input
    class B,C,D,E,F process
    class G,H,I output
```
