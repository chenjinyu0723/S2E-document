# Quick Start

This guide walks you through the core S2E workflow: from raw transcript data to embeddings and pattern prediction.

## Step 1: Import S2E and Create a SubCE Object

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from S2E import SubCE

# Minimal example: one cell, one gene
gene_data = pd.DataFrame({
    'x': [0.1, 0.3, -0.2, 0.5, -0.1],
    'y': [0.2, -0.1, 0.4, -0.3, 0.1],
    'cell': [1, 1, 1, 1, 1],
    'feature_name': ['RPS3'] * 5,
})

cell_boundaries = gpd.GeoSeries(
    Polygon([(-3, -3), (-3, 3), (3, 3), (3, -3)]),
    index=[1]
)
nuclei_boundaries = gpd.GeoSeries(
    Polygon([(-1, -1), (-1, 1), (1, 1), (1, -1)]),
    index=[1]
)

# The 'nuclei' column can be auto-computed if omitted
se = SubCE(gene_data, cell_boundaries, nuclei_boundaries)
```

## Step 2: Normalize to Pseudo-Cell Space

```python
from S2E import processing
processing.normalize(se, num_processes=2)

# Access the normalized layer
norm_layer = se['normalized']
print(norm_layer.uns['points'].head())
```

## Step 3: Metacell Augmentation (Recommended for Sparse Data)

```python
from S2E import aug

# k=19: use 19 auxiliary cells to augment each reference cell
aug.cell_gene_augmentation(se, k=19, num_processes=4)

# Augmented points are stored under 'augmented_points'
aug_pts = se['normalized'].uns['augmented_points']
print(f"Augmented: {len(aug_pts)} points across {aug_pts['cell'].nunique()} cells")
```

## Step 4: Generate Images

```python
from S2E import processing

# Generate PNG images for each cell-gene combination
processing.generate_image_data(
    se,
    layer='normalized',
    pts_key='augmented_points',  # use augmented points
    save_root_path='./images_data',
    dpi=200,
    num_processes=4
)
```

## Step 5: Extract Embeddings

```python
from S2E import analysis

# Get embeddings for all images using the pre-trained model
adata = analysis.get_dataset_embeddings(
    img_root_path='./images_data',
    model_path='./S2E-pattern-model/pytorch_model.bin',  # path to pretrained weights
    batch_size=64,
    num_workers=4
)

print(f"Embedding shape: {adata.shape}")
print(f"Genes: {adata.obs['feature_name'].unique()}")
```

## Step 6: Predict Localization Patterns

```python
# Predict pattern proportions for each image
pattern_adata = analysis.pattern_predict_for_dataset(
    img_root_path='./images_data',
    pretrained_model_path='./S2E-pattern-model/pytorch_model.bin'
)

# Each row is a softmax over 7 patterns (sums to 1)
print(pattern_adata.var['pattern'].tolist())
print(pattern_adata.X[:3])  # first 3 predictions
```

## Step 7: Downstream Analysis

```python
import scanpy as sc

# PCA and UMAP on embeddings
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca')
sc.tl.umap(adata)

# Visualize
from S2E.analysis import plot_umap_from_adata
plot_umap_from_adata(adata, color_by='feature_name', show=True)
```

## Full Workflow with SpatialData

For real spatial omics data (MERFISH, Xenium, etc.):

```python
from S2E.processing import process_spatialdata_for_s2e
from S2E.get import get_gene_data, get_membrane_polygon

# 1. Convert raw data to SpatialData
sdata = process_spatialdata_for_s2e(
    cell_boundaries=cell_gdf,
    nuclei_boundaries=nuc_gdf,
    points_df=points_df,
    num_processes=4,
    verbose=True
)

# 2. Extract data for SubCE
gene_df = get_gene_data(sdata, top_genes_by_expression=500)
cell_bounds, nuc_bounds = get_membrane_polygon(sdata)

# 3. Create SubCE and continue the pipeline
se = SubCE(gene_df, cell_bounds, nuc_bounds)
# ... (continue from Step 2 above)
```
