import pandas as pd

class DataValidator:

    def __init__(
            self,
            required_columns: list
    ):
        self.required_columns = required_columns
    
    def validate_columns(
            self,
            df: pd.DataFrame
    ):
        missing_columns = [
            col for col in self.required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")

        print('Columns validation passed!')
    
    def validate_missing_values(
            self,
            df: pd.DataFrame,
            threshold: float = 0.3
    ):
        
        missing_ratio = df.isnull().mean()

        above_threshold_columns = missing_ratio[missing_ratio > threshold]

        if not above_threshold_columns.empty:
            raise ValueError(f"Columns exceed missing threshold {above_threshold_columns}")
        
        print('Missing value validation passed!')
        
