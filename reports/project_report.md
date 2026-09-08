# Project Report: Metagenomic Biomarker Discovery Pipeline for Colorectal Cancer

## Author
Hemalatha Ponnam

## Project Overview

This repository presents a reproducible public demonstration of downstream microbiome analysis for colorectal-cancer research. The executable demo begins from a small microbial abundance table and focuses on statistical testing, machine-learning analysis, visualization, automated testing, and reproducible workflow practices.

The broader project experience also included upstream metagenomics activities such as FASTQ quality control, adapter trimming, taxonomic classification, and Linux/HPC execution. Those broader components are described separately because they are not fully reproduced by the public scripts in this repository.

## Public Reproducible Demonstration

### Objective

The public demo is designed to show how a microbial abundance table can be validated, analyzed statistically, used in leakage-aware machine-learning workflows, and converted into reproducible outputs.

### Data

The executable workflow uses `data/example_abundance_table.csv`, a small example dataset intended for software demonstration. It does not contain raw patient sequencing data and should not be interpreted as a clinical dataset.

### Statistical Analysis

The public pipeline performs per-feature Kruskal-Wallis testing between the demonstration groups and applies Benjamini-Hochberg false-discovery-rate correction across the tested microbial features. The exported statistics include raw p-values, FDR-adjusted q-values, and a Boolean indicator for `FDR < 0.05`.

These results illustrate workflow behavior rather than validated biological significance. A full research analysis would still require appropriate cohort design, microbiome-specific preprocessing, confounder assessment, and independent validation.

### Machine Learning

The repository includes Random Forest and Support Vector Machine classifiers implemented with scikit-learn pipelines. The train/test split occurs before model preprocessing, and scaling is fitted on the training partition rather than the complete dataset.

The code exports AUC, accuracy, and classification reports as demonstration metrics. Performance values generated from the example data are not presented as estimates of colorectal-cancer diagnostic performance.

### Feature Importance and Visualization

The public workflow exports Random Forest feature importance and generates figures from the actual example inputs and generated model outputs. These plots are intended to demonstrate reproducible result generation rather than identify validated microbial biomarkers.

### Reproducibility and Software Practices

The repository also demonstrates:

- Python scientific programming;
- command-line analysis execution;
- pytest-based automated tests;
- GitHub Actions continuous integration;
- Snakemake workflow orchestration;
- generic SLURM/HPC execution examples; and
- structured result and figure generation.

## Broader Project Experience

The broader metagenomics project context included:

- organization of stool FASTQ data and sample metadata;
- sequencing quality assessment with FastQC;
- adapter and quality trimming with Cutadapt;
- taxonomic classification with Kraken2;
- generation and review of microbial abundance tables;
- additional statistical and biomarker-oriented analyses;
- Random Forest/SVM modeling;
- Linux/HPC execution; and
- workflow optimization and documentation.

These activities represent broader project experience and are not all implemented in the current public repository. Specific dataset-size, model-performance, or time-savings claims are intentionally not presented as public-demo results unless the supporting data and reproducible benchmark are available in the repository.

## Skills Demonstrated

### Public repository

- Python
- pandas / SciPy / statsmodels / scikit-learn
- microbial abundance-table analysis
- Kruskal-Wallis testing
- Benjamini-Hochberg FDR correction
- Random Forest and SVM modeling
- feature-importance analysis
- visualization
- pytest
- GitHub Actions
- Snakemake
- SLURM/HPC concepts
- reproducible scientific computing

### Broader project context

- metagenomic FASTQ processing
- NGS quality control
- Cutadapt
- Kraken2
- taxonomic classification
- microbiome workflow development
- Linux/HPC execution
- biological interpretation and collaboration

## Limitations

- The public repository starts from an example abundance table rather than raw sequencing reads.
- The included example data cannot establish biomarker validity or clinical performance.
- FDR correction improves the feature-wise statistical demonstration but does not replace a complete differential-abundance analysis.
- The current ML evaluation is a portfolio demonstration and lacks external validation.

## Future Improvements

Useful extensions include:

- stronger missing-value and numeric-input validation;
- stratified cross-validation and nested model tuning;
- microbiome-specific filtering and transformation options;
- external public validation data;
- additional automated tests; and
- generated example figures committed directly to the repository.

## Conclusion

This repository demonstrates a careful separation between reproducible public code and broader metagenomics project experience. The public artifact highlights microbiome data analysis, multiple-testing-aware statistical workflow design, machine-learning pipeline construction, reproducibility, testing, CI, and HPC-aware scientific computing without presenting example-data outputs as clinical or biological validation.
