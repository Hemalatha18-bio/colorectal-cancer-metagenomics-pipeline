# Metagenomic Biomarker Discovery Pipeline for Colorectal Cancer

## Overview

This project presents an end-to-end metagenomics pipeline for colorectal cancer biomarker discovery using stool FASTQ sequencing data. The workflow includes raw sequencing quality control, adapter trimming, taxonomic classification, microbial feature extraction, statistical testing, biomarker validation, and machine learning model evaluation.

The project demonstrates skills in NGS data processing, microbiome bioinformatics, statistical analysis, machine learning, reproducible workflows, and cancer-related biological interpretation.

## Objective

The goal of this project was to build a reproducible metagenomic analysis workflow that could:

* Process raw stool FASTQ sequencing files
* Perform sequencing quality control
* Remove adapters and low-quality reads
* Classify microbial reads taxonomically
* Generate microbial abundance feature tables
* Identify candidate microbial biomarkers
* Validate biomarkers using statistical tests
* Train machine learning models for classification
* Interpret microbial features associated with colorectal cancer

## Background

The gut microbiome plays an important role in human health and disease. Changes in microbial community composition have been associated with colorectal cancer and may provide useful biomarkers for disease detection, progression, or biological interpretation.

Metagenomic sequencing allows researchers to profile microbial communities from stool samples. However, raw sequencing data require careful processing before meaningful biological conclusions can be drawn. This project builds a structured pipeline from raw FASTQ data to statistical and machine learning-based biomarker analysis.

## Dataset

This project used stool metagenomic FASTQ data related to colorectal cancer microbiome analysis. The full workflow was designed for large-scale sequencing data and processed more than 25 GB of FASTQ files in the project setting.

Note: Raw sequencing data are not included in this repository. This repository provides the workflow structure, example code, documentation, and portfolio-level demonstration files.

## Tools and Technologies

### Bioinformatics Tools

* FastQC
* Cutadapt
* Kraken2
* FASTQ processing
* Taxonomic classification
* Microbial abundance profiling

### Programming and Workflow

* Python
* R
* Bash
* Linux/HPC
* Git/GitHub

### Machine Learning

* Random Forest
* Support Vector Machine
* Feature importance analysis
* Cross-validation
* AUC evaluation

### Statistics

* ANOVA
* Kruskal-Wallis
* Tukey HSD
* Biomarker validation
* Group comparison analysis

## Workflow

### 1. Raw Data Organization

Raw paired-end or single-end FASTQ files were organized by sample ID and metadata group. Metadata were prepared to define disease/control groups and support downstream statistical and machine learning analyses.

### 2. Quality Control with FastQC

FastQC was used to evaluate sequencing quality. The QC step assessed:

* Per-base sequence quality
* Per-sequence quality scores
* GC content
* Adapter contamination
* Sequence duplication levels
* Overrepresented sequences

This step helped identify whether sequencing reads required trimming or additional filtering.

### 3. Adapter Trimming with Cutadapt

Cutadapt was used to remove adapter sequences and low-quality bases from FASTQ reads. Trimming improved the quality of input reads before taxonomic classification.

### 4. Taxonomic Classification with Kraken2

Kraken2 was used to classify sequencing reads into microbial taxa using reference databases. This step generated taxonomic profiles for each sample.

### 5. Feature Extraction

Kraken2 classification outputs were converted into structured microbial abundance tables. These feature tables represented microbial taxa across samples and were used for statistical and machine learning analysis.

### 6. Data Cleaning and Normalization

Microbial abundance tables were cleaned and normalized before analysis. Low-abundance features and noisy taxa were filtered to improve interpretability and reduce dimensionality.

### 7. Statistical Biomarker Analysis

Statistical tests were applied to identify microbial features that differed between groups:

* ANOVA
* Kruskal-Wallis
* Tukey HSD

These methods helped identify candidate microbial biomarkers associated with colorectal cancer.

### 8. Machine Learning Model Development

Machine learning models were trained using microbial abundance features. Models included:

* Random Forest
* Support Vector Machine

The models were used to evaluate whether microbial profiles could distinguish colorectal cancer-related samples from comparison groups.

### 9. Model Evaluation

Models were evaluated using cross-validation and AUC-based performance metrics. In the project setting, classification models achieved AUC above 0.90.

### 10. Feature Importance and Biological Interpretation

Feature importance methods were used to identify microbial taxa contributing most strongly to model predictions. These candidate biomarkers were interpreted in the context of colorectal cancer microbiome research.

### 11. Workflow Optimization

Preprocessing steps were parallelized where possible, reducing QC-to-feature processing time by approximately 35%.

## Results

Key outcomes of the project included:

* Built an end-to-end metagenomics pipeline for 25+ GB of stool FASTQ data
* Performed quality control using FastQC
* Removed adapters and low-quality regions using Cutadapt
* Classified microbial reads using Kraken2
* Generated microbial abundance feature tables
* Validated microbial biomarkers using ANOVA, Kruskal-Wallis, and Tukey HSD
* Trained Random Forest and SVM classifiers
* Achieved cross-validation AUC above 0.90 in the project setting
* Reduced QC-to-feature processing time by approximately 35% through parallelized preprocessing

## Key Skills Demonstrated

* NGS data processing
* Metagenomic pipeline development
* FASTQ quality control
* Adapter trimming
* Taxonomic classification
* Microbiome feature extraction
* Statistical biomarker validation
* Machine learning for microbiome data
* R/Python-based analysis
* Linux/HPC workflow execution
* Cancer-related biological interpretation
* Reproducible project documentation

## Repository Structure

```text
colorectal-cancer-metagenomics-pipeline/
│
├── README.md
├── data_description.md
├── requirements.txt
├── notebooks/
├── src/
├── figures/
├── results/
├── reports/
├── data/
└── LICENSE
```

## Suggested Folder Details

### data/

Contains synthetic or example data files only. Raw FASTQ files are not included.

### notebooks/

Exploratory notebooks for preprocessing, statistical testing, and model evaluation.

### src/

Reusable scripts for quality control summaries, abundance table processing, biomarker testing, and model training.

### figures/

Workflow diagrams, model performance plots, biomarker visualizations, and example outputs.

### results/

Summary tables for model performance, statistical testing, and candidate biomarkers.

### reports/

Project report and interpretation summary.

## Data Privacy and Availability

Raw sequencing data are not included in this repository because metagenomics datasets can be large and may have usage restrictions. This repository is intended to demonstrate the workflow, project structure, code templates, and portfolio-level documentation.

Users who wish to reproduce this workflow should download appropriate public colorectal cancer microbiome datasets from original sources and follow their citation and usage requirements.

## Limitations

This project was developed in an academic/research setting. Public microbiome datasets may vary in sample size, sequencing depth, metadata completeness, and technical batch effects. The results should be interpreted as research-level findings and not as clinical diagnostic claims.

## Future Improvements

Future improvements could include:

* Adding external validation cohorts
* Using additional taxonomic classifiers
* Incorporating functional profiling
* Testing additional machine learning models
* Packaging the workflow with Snakemake or Nextflow
* Adding automated QC reports
* Building interactive biomarker visualizations
* Expanding analysis to pathway-level microbiome functions

## Portfolio Summary

This project demonstrates my ability to process raw metagenomic sequencing data, build reproducible bioinformatics workflows, apply statistical and machine learning methods, and interpret microbiome biomarkers in a cancer research context.

## Author

Hemalatha Ponnam
M.S. Bioinformatics & Computational Biology
Saint Louis University
Email: [hema22000latha@gmail.com](mailto:hema22000latha@gmail.com)
