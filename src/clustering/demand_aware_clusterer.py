import pandas as pd
import numpy as np
import math
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class DemandAwareClusterer:

    def __init__(
            self,
            vehicle_capacity: int,
            target_vehicles_per_cluster: int = 15,
            random_state: int = 7
    ):
        
        """ 
        Capacity-balanced clustering

        vehicle_capacity:
            Capacity per vehicle
        
        target_vehicles_per_cluster:
            Desired number of vehicles per cluster
        """

        self.vehicle_capacity = vehicle_capacity
        self.target_vehicles_per_cluster = target_vehicles_per_cluster
        self.random_state = random_state
    
    def compute_optimal_cluster_count(
            self,
            df: pd.DataFrame
    ) -> int:
        
        total_demand = df['Demand_Forecast'].sum()
        target_cluster_demand = self.vehicle_capacity * self.target_vehicles_per_cluster
        n_clusters = math.ceil(total_demand/target_cluster_demand)

        return max(n_clusters, 1)

    def cluster(
            self,
            df : pd.DataFrame
    ) -> pd.DataFrame:
        
        df = df.copy()
        n_clusters = self.compute_optimal_cluster_count(df)

        print(f"\n[Clustering]")
        print(f"Total Demand: {df['Demand_Forecast'].sum()}")
        print(f"Vehicle Capacity: {self.vehicle_capacity}")
        print(f"Target vehicles/cluster: {self.target_vehicles_per_cluster}")
        print(f"Computed number of clusters: {n_clusters}")

        # Spatial features only
        spatial_features = df[[
            'Latitude',
            'Longitude'
        ]]

        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(spatial_features)

        kmeans = KMeans(
            n_clusters = n_clusters,
            random_state = self.random_state,
            n_init = 10
        )

        df['Cluster_ID'] = kmeans.fit_predict(scaled_features)
        return df
        


