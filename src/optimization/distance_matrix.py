import numpy as np
import pandas as pd
from src.optimization.cost_function import CostFunction

class DistanceMatrix:

   def __init__(self):
      self.cost_function = CostFunction()

   def build(
         self,
         cluster_df: pd.DataFrame
   ):
      
      size = len(cluster_df)
      matrix = [[0 for i in range(size)] for j in range(size)]
 
      for i in range(size):
         for j in range(size):

            if i == j:
               matrix[i][j] = 0
            else:
               from_node = cluster_df.iloc[i]
               to_node = cluster_df.iloc[j]

               cost = self.cost_function.compute_cost(
                  from_node,
                  to_node
               )

               matrix[i][j] = int(cost)
      
      return matrix

