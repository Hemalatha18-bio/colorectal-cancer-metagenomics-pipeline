#!/bin/bash
#SBATCH --job-name=metagenomics-demo
#SBATCH --output=logs/metagenomics-%j.out
#SBATCH --error=logs/metagenomics-%j.err
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G

# Generic portfolio example only. Adapt modules, environment activation,
# partitions, accounts, paths, and resource requests to the target cluster.

set -euo pipefail

mkdir -p logs results figures

# Example environment activation (replace for your system):
# module load python/3.11
# source .venv/bin/activate

python src/metagenomics_ml_pipeline.py \
  --input data/example_abundance_table.csv \
  --metrics-output results/model_metrics.json \
  --stats-output results/kruskal_wallis_results.csv \
  --importance-output results/random_forest_feature_importance.csv

python src/visualize_microbiome_results.py \
  --input data/example_abundance_table.csv \
  --metrics results/model_metrics.json \
  --importance results/random_forest_feature_importance.csv \
  --output-dir figures
