# Metagenomic Biomarker Discovery Pipeline for Colorectal Cancer

## Overview

This portfolio project documents a colorectal-cancer metagenomics workflow spanning raw sequencing QC, adapter trimming, taxonomic classification, microbial feature generation, statistical testing, and machine-learning analysis.

The **public repository is a reproducible demonstration of selected downstream workflow components** using an example microbial abundance table. Raw FASTQ data and the complete original preprocessing environment are not distributed here, so the public code should not be interpreted as a full reproduction of the broader project.

## Public Repository Scope

The public demo includes:

- microbial abundance-table loading and validation;
- per-feature Kruskal-Wallis testing;
- leakage-safe train/test splitting and model preprocessing;
- Random Forest and SVM classification;
- AUC, accuracy, and classification-report export to JSON;
- Random Forest feature-importance export;
- visualizations generated from the real analysis outputs;
- pytest-based automated tests;
- GitHub Actions continuous integration;
- a generic SLURM submission example; and
- a compact Snakemake workflow for analysis and visualization.

The broader project context included FastQC, Cutadapt, Kraken2, large FASTQ processing, Linux/HPC execution, additional statistical analyses, and workflow optimization. Those broader components are documented here as project context but are not fully reproduced by the current public scripts.

## Data and Privacy

Raw sequencing data are not included. The repository contains example or synthetic demonstration data only. The public demo is intended to show workflow structure and software practices, not to establish biological or clinical performance.

See `data_description.md` for additional notes about the example dataset.

## Technologies

### Bioinformatics context

- FastQC
- Cutadapt
- Kraken2
- FASTQ processing
- Taxonomic classification
- Microbial abundance profiling

### Programming and workflow

- Python
- pandas
- SciPy
- scikit-learn
- matplotlib
- pytest
- GitHub Actions
- Snakemake
- Linux/HPC
- SLURM
- Git/GitHub

### Machine learning and statistics

- Random Forest
- Support Vector Machine
- Kruskal-Wallis testing
- AUC and accuracy evaluation
- Feature-importance analysis

## Repository Structure

```text
colorectal-cancer-metagenomics-pipeline/
├── .github/workflows/ci.yml
├── README.md
├── data_description.md
├── requirements.txt
├── data/
│   └── example_abundance_table.csv
├── src/
│   ├── metagenomics_ml_pipeline.py
│   └── visualize_microbiome_results.py
├── tests/
│   └── test_metagenomics_pipeline.py
├── hpc/
│   └── run_metagenomics_demo.slurm
├── workflow/
│   ├── Snakefile
│   └── config.yaml
├── figures/
├── results/
├── reports/
├── notebooks/
└── LICENSE
```

## How to Run the Public Demo

### 1. Clone the repository

```bash
git clone https://github.com/Hemalatha18-bio/colorectal-cancer-metagenomics-pipeline.git
cd colorectal-cancer-metagenomics-pipeline
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows, use `.venv\\Scripts\\activate`.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the analysis demo

```bash
python src/metagenomics_ml_pipeline.py \
  --input data/example_abundance_table.csv \
  --metrics-output results/model_metrics.json \
  --stats-output results/kruskal_wallis_results.csv \
  --importance-output results/random_forest_feature_importance.csv
```

The code performs the train/test split **before** fitting model preprocessing. Scaling is fitted only on the training partition through scikit-learn pipelines to reduce test-set leakage.

### 5. Generate plots from the actual outputs

```bash
python src/visualize_microbiome_results.py \
  --input data/example_abundance_table.csv \
  --metrics results/model_metrics.json \
  --importance results/random_forest_feature_importance.csv \
  --output-dir figures
```

This produces abundance, model-AUC, and Random Forest feature-importance figures from the example input and generated result files rather than hard-coded performance values.

### 6. Run tests

```bash
pytest -q
```

GitHub Actions runs this test suite automatically on pushes and pull requests targeting `main`.

### 7. Run with Snakemake

```bash
snakemake --snakefile workflow/Snakefile --cores 1
```

The Snakemake workflow connects the example abundance table to model/statistical analysis and final visualization. Paths are defined in `workflow/config.yaml`.

### 8. HPC / SLURM example

A generic submission script is included at:

```text
hpc/run_metagenomics_demo.slurm
```

It is intentionally cluster-neutral. Module names, account/partition settings, environment activation, paths, and resource requests should be adapted to the target HPC system.

## Outputs

The analysis writes:

```text
results/model_metrics.json
results/kruskal_wallis_results.csv
results/random_forest_feature_importance.csv
```

The visualization step writes figures under `figures/`. All generated outputs are based on the included example dataset and should be treated as demonstration results.

## Broader Project Context

The original project methodology included:

1. organization of stool FASTQ data and sample metadata;
2. FastQC quality assessment;
3. adapter and quality trimming with Cutadapt;
4. taxonomic classification with Kraken2;
5. microbial abundance-table generation;
6. filtering and normalization;
7. biomarker-oriented statistical testing;
8. Random Forest/SVM modeling;
9. model evaluation and feature interpretation; and
10. Linux/HPC execution and workflow optimization.

The original work involved larger sequencing datasets and additional analyses. Quantitative claims from that broader work are intentionally **not presented here as reproducible public-demo results unless the corresponding data and code are available in this repository**.

## Limitations

- The public repository starts from an example abundance table rather than raw FASTQ files.
- It does not reproduce the complete FastQC/Cutadapt/Kraken2 workflow.
- Example data cannot establish colorectal-cancer biomarker validity or clinical performance.
- The current statistical demo uses Kruskal-Wallis testing; other analyses from the broader project are not fully implemented here.
- External validation and larger independent cohorts would be required before drawing scientific conclusions.

## Possible Future Extensions

- Add stronger missing-value and numeric-input validation.
- Add cross-validation and hyperparameter tuning to the public ML demo.
- Add safe example documentation for FASTQ preprocessing stages without distributing restricted data or environment-specific settings.
- Add additional automated tests for plotting and workflow execution.
- Add an external public validation dataset when an appropriate dataset and metadata schema are available.

## Skills Demonstrated

This repository demonstrates microbiome data analysis, Python scientific programming, statistical testing, leakage-aware machine-learning workflows, model evaluation, feature-importance analysis, automated testing, CI, workflow orchestration, reproducibility practices, Git/GitHub organization, and familiarity with metagenomics/HPC and SLURM concepts.

## Author

Hemalatha Ponnam  
M.S. Bioinformatics & Computational Biology  
Saint Louis University
