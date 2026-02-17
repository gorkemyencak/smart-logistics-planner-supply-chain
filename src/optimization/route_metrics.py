import pandas as pd

class RouteMetrics:

    @staticmethod
    def compute_route_distance(
        route,
        distance_matrix
    ):
        
        distance = 0

        for i in range(len(route) - 1):
            from_node = route[i]
            to_node = route[i+1]
            distance += distance_matrix[from_node][to_node]
        
        return distance
    
    @staticmethod
    def compute_route_load(
        route,
        demands
    ):
        
        load = 0

        for n in route:
            load += demands[n]
        
        return load
