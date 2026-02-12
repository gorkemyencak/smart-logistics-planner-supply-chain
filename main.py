from src.data.kaggle_loader import KaggleCSVLoader
from src.data.data_validator import DataValidator

def main():
    loader = KaggleCSVLoader(
        dataset_name = "ziya07/smart-logistics-supply-chain-dataset"
    )

    # Downloading the dataset from Kaggle into local directory
    loader.download_dataset()

    # Loading the local dataset from local directory
    df = loader.load_local_csv("smart_logistics_dataset.csv")

    # Data Overview
    loader.data_overview(df)

    # Validating the Dataset
    dataset_columns = df.columns.tolist()

    validator = DataValidator(required_columns=dataset_columns)
    validator.validate_columns(df)
    validator.validate_missing_values(df)
    
if __name__ == '__main__':
    main()