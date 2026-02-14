import pandas as pd

class DemandGenerator:
    def __init__(
            self,
            demand_col: str
    ):
        self.demand_col = demand_col
    
    def extract_demands(
            self,
            df: pd.DataFrame
    ) -> list:
        return df[self.demand_col].tolist()
