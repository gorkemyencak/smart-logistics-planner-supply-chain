import pandas as pd
from pathlib import Path

class DataPreprocessor:

    def __init__(
            self,
            output_dir: str = "data/processed" 
    ):
        project_root = Path(__file__).resolve().parents[2]
        self.output_dir = project_root / output_dir
        self.output_dir.mkdir(parents = True, exist_ok = True)

    
    def clean(
            self,
            df: pd.DataFrame
    ) -> pd.DataFrame:
        
        df = df.drop_duplicates()
        return df
    
    def convert_datetime(
            self,
            df: pd.DataFrame,
            datetime_columns: list
    ) -> pd.DataFrame:
        
        for c in datetime_columns:
            df[c] = pd.to_datetime(
                df[c],
                errors = 'coerce'
            )
        
        return df
    
    def save_processed(
            self,
            df: pd.DataFrame,
            file_name: str
    ):
        file_path = self.output_dir / file_name
        df.to_csv(
            file_path, 
            index = False
        )
        
        print(f"Processed dataset saved to {file_path}")