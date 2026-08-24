# Metagenomic Biomarker Discovery Pipeline for Colorectal Cancer

## Overview

This portfolio project documents a colorectal-cancer metagenomics workflow spanning raw sequencing QC, adapter trimming, taxonomic classification, microbial feature generation, statistical testing, and machine-learning analysis.

The **public repository is a reproducible demonstration of selected downstream workflow components** using an example microbial abundance table. Raw FASTQ data and the complete original preprocessing environment are not distributed here, so the public code should not be interpreted as a full reproduction of the broader project.

## Public Repository Scope

The public demo currently includes:

- microbial abundance-table loading and validation;
- per-feature Kruskal-Wallis testing;
- leakage-safe train/test splitting and model preprocessing;
- Random Forest and SVM classification;
- AUC, accuracy, and classification-report export to JSON;
- Random Forest feature-importance export; and
- example visualization/documentation assets.

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

### Programming and analysis

- Python
- pandas
- SciPy
- scikit-learn
- Linux/HPC
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
├── README.md
├── data_description.md
├── requirements.txt
├── data/
│   └── example_abundance_table.csv
├── src/
│   ├── metagenomics_ml_pipeline.py
│   └── visualize_microbiome_results.py
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

## Outputs

The public demo writes:

```text
results/model_metrics.json
results/kruskal_wallis_results.csv
results/random_forest_feature_importance.csv
```

These outputs are generated from the included example dataset and should be treated as demonstration results.

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

## Planned Improvements

- Make visualization scripts read directly from generated result files.
- Add automated tests and GitHub Actions CI.
- Add a generic SLURM example for HPC execution.
- Add a compact Snakemake or Nextflow workflow for the public demo.
- Add stronger missing-value and numeric-input validation.
- Add cross-validation to the public ML demonstration.
- Add safe example documentation for FASTQ preprocessing stages without distributing restricted data or environment-specific settings.

## Skills Demonstrated

This repository demonstrates microbiome data analysis, Python scientific programming, statistical testing, leakage-aware machine-learning workflows, model evaluation, feature-importance analysis, reproducibility practices, Git/GitHub organization, and familiarity with metagenomics/HPC workflow concepts.

## Author

Hemalatha Ponnam  
M.S. Bioinformatics & Computational Biology  
Saint Louis University
