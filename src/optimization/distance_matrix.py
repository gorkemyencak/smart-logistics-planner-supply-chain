import numpy as np
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

class DistanceMatrix:

   @staticmethod
   def compute_euclidean(
      df: pd.DataFrame
   ) -> np.ndarray:
      """ Computes full nxn Euclidean distance matrix """

      coordinates = df[['Latitude', 'Longitude']].copy().to_numpy()

      diff = coordinates[:, np.newaxis, :] - coordinates[np.newaxis, :, :]
      dist_matrix = np.sqrt(
         (diff**2)
         .sum(axis=2)
      )

      return dist_matrix
   
   @staticmethod
   def compute_scaled(
      df: pd.DataFrame,
      scale_factor: int = 1000
   ) -> np.ndarray:
      """ Returns scaled integer distance matrix """

      matrix = DistanceMatrix.compute_euclidean(df)
      return (matrix * scale_factor).astype(int)

