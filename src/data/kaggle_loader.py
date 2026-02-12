import os
import pandas as pd
from pathlib import Path
from src.data.kaggle_downloader import KaggleDownloader

class KaggleCSVLoader:

    def __init__(
            self,
            dataset_name: str,
            data_dir: str = 'data/raw'
    ):
        self.dataset_name = dataset_name

        project_root = Path(__file__).resolve().parents[2]

        self.data_dir = project_root / data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.downloader = KaggleDownloader(
            dataset_name = self.dataset_name,
            download_path = self.data_dir
        )

    def download_dataset(self):
        
        if not any(self.data_dir.iterdir()):
            self.downloader.download()
        else:
            print('Dataset already exists! Skipping data downloading step..')


    def load_local_csv(
            self,
            file_name: str
    ) -> pd.DataFrame:
        
        """ Loading CSV from local raw data directory """
        file_path = self.data_dir / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist!")
        
        df = pd.read_csv(file_path)
        return df
    
    def save_dataframe(
            self, 
            df: pd.DataFrame,
            file_name: str
    ):
        
        """ Saving dataframe to raw data directory """
        file_path = self.data_dir / file_name
        df.to_csv(
            file_path,
            index=False
        )
    
    def data_overview(
            self,
            df: pd.DataFrame
    ):
        print('Shape:', df.shape)
        print('\nColumns:', df.columns)
        print('\nMissing values:', df.isnull().sum())
