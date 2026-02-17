import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class DemandAwareClusterer:

    def __init__(
            self,
            n_clusters: int
    ):
        
        """ Spatial clustering considers only Latitude and Longitude, but the Demand Forecast; therefore a Demand Aware Clustering strategy is needed to avoid fleet imbalance """

        self.n_clusters = n_clusters

    def cluster(
            self,
            df : pd.DataFrame
    ):
        
        features = df[[
            'Latitude', 
            'Longitude',
            'Demand_Forecast'
        ]]

        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        kmeans = KMeans(
            n_clusters = self.n_clusters,
            random_state = 7,
            n_init = 10
        )

        df['Cluster_ID'] = kmeans.fit_predict(scaled_features)

        return df
        


