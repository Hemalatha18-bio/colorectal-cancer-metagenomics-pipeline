# Data Description

## Project

Metagenomic Biomarker Discovery Pipeline for Colorectal Cancer

## Overview

This project uses stool metagenomic sequencing data to identify microbial features associated with colorectal cancer. The workflow begins with raw FASTQ sequencing files and continues through quality control, adapter trimming, taxonomic classification, microbial feature extraction, statistical testing, and machine learning model evaluation.

## Data Types

### 1. Raw FASTQ Sequencing Data

FASTQ files represent raw metagenomic sequencing reads generated from stool samples.

Typical FASTQ inputs may include:

* Paired-end FASTQ files
* Single-end FASTQ files
* Sample-level metadata
* Disease/control grouping information

### 2. Sample Metadata

Metadata are required to connect each sequencing sample to its biological or clinical group.

Example metadata fields:

* Sample ID
* Group label
* Disease status
* Sequencing batch
* Read type
* Notes on sample quality

### 3. Taxonomic Classification Outputs

Kraken2 outputs were used to classify sequencing reads into microbial taxa.

Example output categories:

* Taxon ID
* Scientific name
* Read count
* Relative abundance
* Sample ID

### 4. Microbial Abundance Tables

Taxonomic classification outputs were converted into abundance tables for downstream statistics and machine learning.

Example feature table structure:

* Rows: samples
* Columns: microbial taxa or features
* Values: read counts or normalized abundance values
* Label column: disease/control group

## Data Availability

Raw FASTQ files are not included in this repository.

This repository is intended to demonstrate:

* Workflow structure
* Bioinformatics methodology
* Code templates
* Example analysis logic
* Portfolio-level documentation

Large sequencing datasets should be downloaded from their original public sources and cited appropriately.

## Why Raw Data Is Not Included

Raw sequencing files are not included because:

* FASTQ files are large
* Dataset usage terms vary
* Some datasets may require controlled access
* The repository is meant for workflow demonstration
* Public repositories should avoid unnecessary large data storage

## Example Data

This repository may include small synthetic example files to demonstrate code functionality. These files are not real patient data and should only be used for testing scripts.

## Processing Workflow

The data workflow includes:

1. Organize FASTQ files and metadata
2. Run FastQC for sequencing quality control
3. Trim adapters and low-quality reads using Cutadapt
4. Classify reads using Kraken2
5. Convert classification outputs into abundance tables
6. Clean and normalize microbial feature tables
7. Perform statistical biomarker testing
8. Train machine learning classifiers
9. Evaluate model performance
10. Interpret candidate microbial biomarkers

## Ethical and Privacy Considerations

This repository does not include protected health information, private patient data, sample identifiers, or confidential clinical records.

## Reproducibility Notes

To reproduce a similar workflow, users should:

* Download public colorectal cancer microbiome datasets
* Follow original dataset citation requirements
* Use consistent metadata formatting
* Run QC and preprocessing tools in a reproducible environment
* Document software versions and database versions

## Author

Hemalatha Ponnam
M.S. Bioinformatics & Computational Biology
Saint Louis University
Email: [hema22000latha@gmail.com](mailto:hema22000latha@gmail.com)
