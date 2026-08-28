# Obtaining the Olist data

The project expects the CSV files from the [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) in `data/raw/`.

## Kaggle CLI

1. Create a Kaggle API token in your Kaggle account and configure `~/.kaggle/kaggle.json`.
2. From the project root run:

   ```bash
   kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip
   ```

## Manual download

Download the dataset from Kaggle, unzip it, and copy the CSV files directly into `data/raw/`. Do not commit this directory: the repository ignores it.

## Offline demo data

To exercise the complete pipeline without the source data, run `python -m src.generate_sample_data`. It creates a small, deterministic relational sample with the same required Olist file names and columns. It is illustrative only and must not be used for business conclusions.
