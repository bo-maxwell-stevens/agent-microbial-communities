# Analysis Feasibility Matrix

Generated: 2026-05-19T13:22:43.626749+00:00  
Git commit: `eb784829b2b24d988d2b07e12a30765935b6fdcc`

Current basis:
- META n=99
- Full-overlap META+AMF+BAC+EUK+ITS n=84
- Feature dimensionality remains extreme especially BAC, requiring strict reduction.

| Analysis class | Feasibility score | Key assumptions | Main risks and reviewer criticism | Publishable now |
|---|---|---|---|---|
| compositional ordination | Moderate feasibility | Requires prevalence filtering, compositional transforms, and confounder control | Manageable with constrained design and blocked permutation or CV | Yes |
| PERMANOVA | Moderate feasibility | Requires prevalence filtering, compositional transforms, and confounder control | Manageable with constrained design and blocked permutation or CV | Yes |
| dbRDA | Moderate feasibility | Requires prevalence filtering, compositional transforms, and confounder control | Manageable with constrained design and blocked permutation or CV | Yes |
| variation partitioning | Low feasibility | Requires aggressive feature reduction and strict blocked validation | High overfitting or unstable estimates under current n/p | No |
| RF + SHAP | Low feasibility | Requires aggressive feature reduction and strict blocked validation | High overfitting or unstable estimates under current n/p | No |
| multi-kingdom integration | Moderate feasibility | Requires prevalence filtering, compositional transforms, and confounder control | Manageable with constrained design and blocked permutation or CV | Yes |
| co-occurrence networks | Not recommended | Large n, stable associations, compositional correction | High false-positive risk with sparse compositional counts and n about 84 overlap | No |
| latent embeddings | Moderate feasibility | Requires prevalence filtering, compositional transforms, and confounder control | Manageable with constrained design and blocked permutation or CV | Yes |
| sparse PCA | Moderate feasibility | Requires prevalence filtering, compositional transforms, and confounder control | Manageable with constrained design and blocked permutation or CV | Yes |
| CCA/RDA | Low feasibility | Requires aggressive feature reduction and strict blocked validation | High overfitting or unstable estimates under current n/p | No |
| distance-decay analyses | Moderate feasibility | Requires prevalence filtering, compositional transforms, and confounder control | Manageable with constrained design and blocked permutation or CV | Yes |
| beta diversity partitioning | Moderate feasibility | Requires prevalence filtering, compositional transforms, and confounder control | Manageable with constrained design and blocked permutation or CV | Yes |
| stochastic vs deterministic assembly metrics | Low feasibility | Requires aggressive feature reduction and strict blocked validation | High overfitting or unstable estimates under current n/p | No |

Detailed machine-readable version:
- `results/feasibility/analysis_feasibility_matrix.csv`

## Key risk themes
- Pseudoreplication and confounding must be controlled with blocked designs.
- Compositionality risks are high for raw-count distance or network approaches.
- Overfitting risk is high for supervised models unless reduced to low-dimensional representations with strict validation.

## Decision summary
- Most defensible now: constrained distance-based and reduced-space multivariate analyses.
- Least defensible now: unconstrained taxon-level cross-kingdom network inference on n about 84.
