import subprocess
from pathlib import Path

class KaggleDownloader:

    def __init__(
            self,
            dataset_name: str, 
            download_path: Path
    ):
        self.dataset_name = dataset_name
        self.download_path = download_path
        self.download_path.mkdir(parents=True, exist_ok=True)
    
    def download(self):
        print(f"Downloading Kaggle dataset: {self.dataset_name}")

        command = [
            'kaggle',
            'datasets',
            'download',
            '-d',
            self.dataset_name,
            '-p',
            str(self.download_path),
            '--unzip'
        ]

        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

        print('Download completed!')

