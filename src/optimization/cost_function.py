import numpy as np

class CostFunction:
    """
    Multi-objective cost calculation for routing.
    It combines:
        * Euclidean distance
        * Traffic penalty
        * Waiting time penalty
        * Delay penalty
    """

    def __init__(
            self,
            distance_weight: float = 1.0,
            traffic_weight: float = 0.5,
            waiting_weight: float = 0.3,
            delay_weight: float = 0.5
    ):
        
        self.distance_weight = distance_weight
        self.traffic_weight = traffic_weight
        self.waiting_weight = waiting_weight
        self.delay_weight = delay_weight
    
    def euclidean_distance(
            self,
            lat1,
            lon1,
            lat2,
            lon2
    ):
        return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
    
    def traffic_penalty(
            self,
            traffic_status
    ):
        traffic_map = {
            'Clear': 1,
            'Detour': 2,
            'Heavy': 3
        }
        
        return traffic_map.get(traffic_status, 1)
    
    def compute_cost(
            self,
            from_node,
            to_node
    ):
        
        distance = self.euclidean_distance(
            from_node['Latitude'],
            from_node['Longitude'],
            to_node['Latitude'],
            to_node['Longitude']
        )

        traffic = self.traffic_penalty(to_node.get('Traffic_Status', 'Clear'))
        waiting_time = to_node.get('Waiting_Time', 0)
        delay = to_node.get('Logistics_Delay', 0)

        total_cost = (
            self.distance_weight * distance +
            self.traffic_weight * traffic +
            self.waiting_weight * waiting_time + 
            self.delay_weight * delay
        )

        return int(1000 * total_cost) # scaled integer, since OR tools cannot handle float cost for distances.
