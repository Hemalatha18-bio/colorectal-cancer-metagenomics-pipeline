# Project Report: Metagenomic Biomarker Discovery Pipeline for Colorectal Cancer

## Author
Hemalatha Ponnam

## Project Overview

This project developed an end-to-end metagenomic biomarker discovery workflow for colorectal cancer using stool FASTQ sequencing data. The workflow processed raw sequencing reads through quality control, adapter trimming, taxonomic classification, feature extraction, statistical testing, and machine learning model evaluation.

The goal was to identify microbial features that may help distinguish colorectal cancer-associated microbiome profiles from control profiles.

## Background

The gut microbiome plays an important role in human health and disease. Changes in microbial community structure have been reported in colorectal cancer and may provide useful biological insights or candidate biomarkers.

Metagenomic sequencing allows researchers to study microbial communities from stool samples, but raw FASTQ data must be carefully processed before downstream analysis. This project demonstrates how microbiome sequencing data can be converted into interpretable microbial features for statistical and machine learning analysis.

## Objective

The main objectives of this project were to:

1. Process stool metagenomic FASTQ data.
2. Perform sequencing quality control.
3. Remove adapters and low-quality reads.
4. Classify microbial reads taxonomically.
5. Generate microbial abundance tables.
6. Identify differentially abundant microbial taxa.
7. Train machine learning models for classification.
8. Interpret candidate microbial biomarkers.

## Methods

### 1. FASTQ Quality Control

FastQC was used to evaluate raw sequencing quality, including:

- Per-base quality scores
- GC content
- Adapter contamination
- Sequence duplication
- Overrepresented sequences

### 2. Adapter Trimming

Cutadapt was used to remove adapter sequences and low-quality regions from FASTQ reads before downstream classification.

### 3. Taxonomic Classification

Kraken2 was used to classify sequencing reads into microbial taxa using reference databases.

### 4. Feature Table Generation

Kraken2 outputs were converted into microbial abundance tables. These tables were structured with samples as rows and microbial taxa as columns.

### 5. Statistical Analysis

Candidate microbial biomarkers were evaluated using statistical methods including:

- ANOVA
- Kruskal-Wallis
- Tukey HSD

These methods helped identify microbial taxa with different abundance patterns between groups.

### 6. Machine Learning

Random Forest and Support Vector Machine classifiers were trained using microbial abundance features. Model performance was evaluated using cross-validation and AUC.

### 7. Feature Importance

Feature importance methods were used to identify microbial taxa that contributed most strongly to classification performance.

## Results

Key results from the project included:

- Processed 25+ GB of stool FASTQ data.
- Built a complete QC-to-feature metagenomics workflow.
- Used FastQC, Cutadapt, and Kraken2 for preprocessing and classification.
- Generated microbial abundance feature tables.
- Identified candidate microbial biomarkers using statistical testing.
- Trained Random Forest and SVM classifiers.
- Achieved cross-validation AUC above 0.90 in the project setting.
- Reduced QC-to-feature processing time by approximately 35% through parallelized preprocessing.

## Skills Demonstrated

This project demonstrates experience in:

- Metagenomic data analysis
- FASTQ processing
- NGS quality control
- Taxonomic classification
- Microbiome feature extraction
- Statistical biomarker validation
- Random Forest and SVM modeling
- Python and R analysis
- Linux/HPC workflow execution
- Reproducible bioinformatics documentation
- Cancer microbiome research

## Limitations

Raw sequencing data are not included in this public repository. The repository uses simplified example files and workflow documentation for portfolio demonstration. Public microbiome datasets may vary in sequencing depth, sample size, metadata quality, and batch effects.

The results should be interpreted as research-level findings and not as clinical diagnostic claims.

## Future Improvements

Future improvements could include:

- Adding external validation datasets
- Using additional taxonomic classifiers
- Adding functional profiling
- Packaging the workflow with Snakemake or Nextflow
- Creating automated QC reports
- Adding interactive visualization dashboards
- Expanding the analysis to pathway-level microbiome functions

## Conclusion

This project demonstrates how raw metagenomic sequencing data can be processed and analyzed to identify microbial features associated with colorectal cancer. It highlights skills in microbiome bioinformatics, NGS workflows, statistical analysis, machine learning, and biological interpretation.
