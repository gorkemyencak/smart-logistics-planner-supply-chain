import numpy as np
import pandas as pd

class DistanceMatrix:

    def __init__(
            self,
            latitude_col: str,
            longitude_col: str
    ):
        self.latitude_col = latitude_col
        self.longitude_col = longitude_col
    
    def haversine(
            self,
            lat1,
            lon1,
            lat2,
            lon2
    ):
        
        R = 6371 # Earth radius in km

        lat1, lon1, lat2, lon2 = map(
            np.radians, 
            [lat1, lon1, lat2, lon2]
        )

        dist_lat = lat2 - lat1
        dist_lon = lon2 - lon1

        a = (
            np.sin(dist_lat/2)**2 +
            np.cos(lat1) * np.cos(lat2) * np.sin(dist_lon/2)**2
        )

        c = 2 * np.arcsin(np.sqrt(a))

    def build_matrix(
            self,
            df: pd.DataFrame
    ) -> np.ndarray:
        
        coordinates = df[[self.latitude_col, self.longitude_col]].values
        n = len(coordinates)

        matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                matrix[i][j] = self.haversine(
                    coordinates[i][0], coordinates[i][1],
                    coordinates[j][0], coordinates[j][1]
                )
        
        return matrix

