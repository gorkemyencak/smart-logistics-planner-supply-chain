import pandas as pd
from sklearn.cluster import KMeans

class NodeClusterer:

    def __init__(
            self, 
            n_clusters: int = 3,
            random_state: int = 7
    ):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = KMeans(
            n_clusters = self.n_clusters,
            random_state = self.random_state
        )

    def fit_predict(
            self,
            df: pd.DataFrame
    ) -> pd.DataFrame:
        
        coordinates = df[['Latitude', 'Longitude']]
        df['Cluster_ID'] = self.model.fit_predict(coordinates)

        return df