# Data Description

## Project
Metagenomic Biomarker Discovery Pipeline for Colorectal Cancer

## Public Demo Data

The executable public demonstration in this repository starts from:

`data/example_abundance_table.csv`

This file is a small example microbial abundance table intended for software testing, workflow demonstration, and portfolio documentation. It is not raw patient sequencing data and should not be used to draw biological or clinical conclusions.

The public demo does **not** begin from FASTQ files. Raw sequencing QC, adapter trimming, taxonomic classification, and complete upstream feature-generation steps belong to the broader project context and are not fully reproduced by the current public scripts.

## Expected Table Structure

The example abundance table is organized with samples as rows and microbial features as columns. The analysis code expects:

- a binary group label column, by default `label`;
- an optional sample identifier column, by default `SampleID`; and
- numeric microbial feature columns used for statistical testing and machine-learning analysis.

The public scripts load and validate this table, identify feature columns, perform per-feature statistics, and train demonstration classifiers.

## What Is Not Included

This repository does not include:

- raw stool FASTQ sequencing files;
- protected health information or private patient records;
- original project sample identifiers;
- complete FastQC outputs;
- original Cutadapt outputs;
- Kraken2 databases or full taxonomic-classification outputs;
- restricted or lab-owned datasets; or
- a complete reproduction of the broader upstream preprocessing environment.

## Broader Project Data Context

The broader metagenomics project involved data types and workflow stages such as:

- paired-end stool FASTQ sequencing data;
- sample metadata and disease/control grouping;
- sequencing QC outputs;
- adapter- and quality-trimmed reads;
- Kraken2 taxonomic-classification results;
- microbial count or abundance tables; and
- downstream statistical and machine-learning analysis tables.

Those data types describe broader project experience. They should not be inferred to be present in this public repository unless a corresponding file or executable workflow step is included here.

## Public Processing Workflow

The reproducible public workflow is:

1. Load `data/example_abundance_table.csv`.
2. Validate the label and feature columns.
3. Run feature-wise Kruskal-Wallis testing.
4. Split the example data for model training and evaluation.
5. Train Random Forest and SVM demonstration pipelines.
6. Export model metrics and Random Forest feature importance.
7. Generate figures from the example input and generated outputs.
8. Optionally orchestrate the workflow using Snakemake or submit the demonstration through the generic SLURM example.

## Interpretation

Any statistics, feature rankings, AUC values, or accuracy values generated from the included example dataset are demonstration outputs. They are intended to show that the code and workflow execute reproducibly, not to establish colorectal-cancer biomarker validity or diagnostic performance.

A research-grade microbiome analysis would require appropriate cohort design, metadata review, preprocessing and normalization choices, multiple-testing correction, confounder assessment, and independent validation.

## Reproducibility Notes

Users who want to extend the repository with public real-world data should:

- obtain data from an appropriate public source and follow its citation and usage requirements;
- document accession identifiers and metadata definitions;
- record software and reference-database versions;
- keep preprocessing and filtering choices explicit;
- avoid committing restricted, unpublished, or patient-identifiable data; and
- clearly distinguish generated research findings from example-data demonstrations.

## Author

Hemalatha Ponnam  
M.S. Bioinformatics & Computational Biology  
Saint Louis University
