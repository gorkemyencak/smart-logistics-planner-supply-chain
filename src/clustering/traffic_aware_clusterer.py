import numpy as np
import pandas as pd
import math
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class TrafficAwareClusterer:
    def __init__(
            self,
            vehicle_capacity: int,
            target_vehicles_per_cluster: int,
            random_state: int = 7 
    ):
        
        self.vehicle_capacity = vehicle_capacity
        self.target_vehicles_per_cluster = target_vehicles_per_cluster
        self.random_state = random_state
    
    def _encode_traffic(
            self,
            df: pd.DataFrame
    ):
        """ Encoding Traffic_Status column numerically """
        traffic_map = {
            'Clear': 1,
            'Detour': 2,
            'Heavy': 3
        }

        if df['Traffic_Status'].dtype == 'str':
            return df['Traffic_Status'].map(traffic_map).fillna(1)
        
        else:
            return df['Traffic_Status']
    
    def compute_number_of_clusters(
            self,
            df: pd.DataFrame
    ):
        
        total_demand = df['Demand_Forecast'].sum()
        total_vehicles = math.ceil(
            total_demand / self.vehicle_capacity
        )

        num_clusters = math.ceil(
            total_vehicles / self.target_vehicles_per_cluster
        )

        print("\nTraffic-Aware Clusterer")
        print(f"Total Demand: {total_demand}")
        print(f"Vehicle Capacity: {self.vehicle_capacity}")
        print(f"Estimated Vehicles: {total_vehicles}")
        print(f"Target vehicles/cluster: {self.target_vehicles_per_cluster}")
        print(f"Computed number of clusters: {num_clusters}")

        return num_clusters
    
    def cluster(
            self,
            df: pd.DataFrame
    ):
        
        df = df.copy()
        num_clusters = self.compute_number_of_clusters(df)

        # Encode traffic status
        df['Traffic_Encoded'] = self._encode_traffic(df)

        # Build feature matrix
        features = df[[
            "Latitude",
            "Longitude",
            "Demand_Forecast",
            "Traffic_Encoded",
            "Waiting_Time"
        ]]

        # Scaling features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Weighted clustering
        scaled_features[:, 2] *= 2.0    # Demand weight
        scaled_features[:, 3] *= 1.5    # Traffic weight
        scaled_features[:, 4] *= 1.2    # Waiting time weight

        kmeans = KMeans(
            n_clusters = num_clusters,
            n_init = 10,
            random_state = self.random_state
        )

        df['Cluster_ID'] = kmeans.fit_predict(scaled_features)

        print("\nCluster Distribution")
        print(df['Cluster_ID'].value_counts().sort_index())

        return df


