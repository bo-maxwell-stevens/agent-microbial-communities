# Agent Goals and Scientific Operating Principles

## Project Purpose

This repository contains integrated microbial community datasets and associated environmental metadata intended for exploratory ecological analysis, predictive modeling, and autonomous or semi-autonomous scientific workflows.

The long-term goal is to develop reproducible, interpretable, and biologically meaningful analyses of microbial community structure and function across multiple microbial groups, including:

- bacteria
- AMF
- ITS fungi
- microbial eukaryotes

The project may eventually support:
- autonomous scientific exploration
- AI-guided hypothesis generation
- reproducible machine learning pipelines
- ecological network analyses
- Denario or multi-agent experimentation systems

---

# Core Scientific Priorities

Analyses should prioritize:

1. Biological interpretability
2. Statistical rigor
3. Reproducibility
4. Ecological realism
5. Transparent assumptions
6. Robust validation

The goal is not merely maximizing predictive performance. Analyses should seek ecologically meaningful and interpretable patterns.

---

# Preferred Analytical Philosophy

## Interpretability Over Black-Box Optimization

Prefer methods that can be interpreted biologically.

Examples:
- Random Forest + SHAP
- Partial dependence
- Feature importance
- Ordination methods
- Correlation structure
- Network modularity

Highly opaque models should generally not be prioritized unless they substantially improve performance or reveal novel structure.

---

# Validation Philosophy

## Avoid Data Leakage

Prevent leakage between training and testing datasets.

Environmental, spatial, temporal, or site-level dependence structures should be considered carefully.

---

## Prefer Group-Aware Validation

Where appropriate, use:
- grouped cross-validation
- site-level splits
- blocking structures

Avoid inflated predictive performance caused by pseudoreplication or correlated samples.

---

## Repeated Validation Preferred

Repeated grouped CV or repeated holdout validation is preferred over single train/test splits when computationally feasible.

Preferred reporting:
- mean performance
- confidence intervals
- variability across splits

---

# Ecological Interpretation Principles

## Correlation Does Not Imply Mechanism

Associations discovered by machine learning should not automatically be interpreted causally.

Generated hypotheses should be treated as candidate ecological relationships requiring validation.

---

## Prioritize Cross-Kingdom Interactions

Potentially important relationships may occur between:
- bacteria and fungi
- fungi and AMF
- protists and fungi
- environmental gradients and microbial structure

Exploration of integrated community relationships is encouraged.

---

## Rare Taxa Handling

Rare taxa may contain ecological signal but can also introduce instability.

Filtering, prevalence thresholds, or dimensionality reduction may be appropriate depending on analytical goals.

Document all filtering choices clearly.

---

# Data Handling Principles

## Raw Data Preservation

Never modify original raw input data files.

Derived data products should be written to:
- results/
- outputs/
- intermediate/

while preserving source files unchanged.

---

## Reproducibility

All analyses should be:
- scriptable
- reproducible
- version controlled

Avoid manual spreadsheet manipulation whenever possible.

---

## Logging and Documentation

Important analyses should generate:
- logs
- summaries
- metadata
- parameter descriptions
- reproducible outputs

Analytical decisions should be documented.

---

# Machine Learning Preferences

Preferred initial methods include:
- Random Forest
- Gradient boosting
- SHAP interpretation
- Ordination
- Clustering
- Ecological network analysis

Potential future methods:
- representation learning
- embeddings
- latent ecological gradients
- autonomous hypothesis generation

---

# Computational Principles

## Safety

Autonomous agents should:
- avoid destructive actions
- avoid deleting important files
- avoid overwriting source datasets
- prefer creating new outputs

---

## Git Workflow

Prefer:
- branch-based development
- pull requests
- commit summaries
- incremental changes

Avoid direct modification of stable workflows without logging or version control.

---

# Desired Agent Behaviors

Agents are encouraged to:

- inspect repository structure
- summarize datasets
- identify preprocessing requirements
- propose analyses
- generate exploratory reports
- detect potential statistical issues
- suggest reproducible workflows
- identify possible ecological hypotheses

Agents should avoid:
- overclaiming biological interpretation
- treating correlation as causation
- silently modifying source data
- generating unreproducible workflows
- hiding uncertainty

---

# Long-Term Vision

This repository may evolve into a semi-autonomous microbial ecology research platform integrating:

- local computation
- VPS orchestration
- GitHub versioning
- AI-assisted coding
- autonomous workflows
- HPC integration
- ecological machine learning
- manuscript scaffolding
- literature-aware agents

The system should remain scientifically rigorous, interpretable, and reproducible as autonomy increases.
