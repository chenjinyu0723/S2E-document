# Background

## Scientific Motivation

The spatial organization of molecules within a cell is fundamental to their function. While current computational frameworks have advanced spatial analysis at the subcellular level by defining domains and quantifying colocalization, a critical gap remains in generating gene embeddings that directly capture the nuanced spatial distribution patterns of transcripts.

S2E bridges this gap by leveraging **Vision Transformers** (ViTs) to encode subcellular spatial patterns of genes into a unified embedding space.

## Computational Challenges

As resolution approaches the sub-micron scale, spatial transcriptomics data analysis faces formidable challenges:

- **Extreme sparsity**: Often only a handful of RNA transcripts per gene are captured within a single cell
- **Unstructured point-cloud nature**: Raw transcript coordinates lack the regular grid structure needed for conventional analysis
- **Scale variance**: Cells vary dramatically in size and shape

Traditional statistical frameworks struggle to decode the latent functional semantics embedded within the physical landscape of these sparse point patterns.

## The S2E Solution

S2E addresses these challenges through a multi-stage pipeline:

1. **Data Integration** — Integrates single-molecule coordinates from high-throughput spatial omics with membrane morphology (polygons) into a SpatialData-compatible format
2. **Spatial Normalization** — Maps raw transcripts to pseudo-cells with standardized geometry (nucleus radius=1, cell radius=2.783)
3. **Metacell Augmentation** — Physically superimposes biological signals from multiple independent cells onto the standardized pseudo-cell coordinate system, dramatically increasing effective transcript density
4. **Image Rendering** — Transforms augmented transcript coordinates into image representations
5. **ViT Embedding** — Processes images through a pre-trained Vision Transformer to generate gene-specific embeddings at single-cell resolution
6. **Downstream Analysis** — Enables quantitative assessment of subcellular localization pattern heterogeneity

## Seven Canonical Localization Patterns

The S2E pre-trained model recognizes seven distinct subcellular RNA localization patterns:

| Pattern | Description |
|---------|-------------|
| **Intranuclear** | Uniform distribution within the nucleus |
| **Nuclear edge** | Enrichment at the nuclear membrane |
| **Perinuclear** | Cytoplasmic bias toward nucleus, density decays with distance |
| **Extranuclear** | Random cytoplasmic distribution |
| **Cell edge** | Enrichment at the cell membrane |
| **Pericellular** | Cytoplasmic ring, density decreases toward nucleus |
| **Foci** | Dense aggregates representing molecular clusters |

## Pre-trained Model

The S2E pattern prediction model was pre-trained on **1,050,748 simulated instances** using 4× RTX 4090 GPUs for 22 epochs (~8 hours). The model backbone is `microsoft/swinv2-base-patch4-window16-256` with `google/vit-base-patch16-224` as an alternative.

## Key Findings

- **Metacell augmentation** (k≥3) reliably distinguishes fine-grained gene-specific spatial features even under extreme sparsity (as few as 16 transcripts per instance)
- **Empirical threshold**: ~200 transcripts per metacell achieves sensitive gene-level differentiation
- S2E embeddings successfully capture **drug-induced spatial reorganization** in iPSC cardiomyocytes and **ER stress time-course responses** in HeLa cells

## References

The S2E framework demonstrates that image-based representation learning can effectively capture and compare subcellular RNA localization patterns, opening new avenues for understanding the functional roles of RNA spatial organization in health and disease.
