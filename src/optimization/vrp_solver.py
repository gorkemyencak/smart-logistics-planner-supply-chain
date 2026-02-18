import math
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from src.optimization.distance_matrix import DistanceMatrix

class VRPsolver:

    def __init__(
            self, 
            vehicle_capacity: int,
            vehicle_fixed_cost: int = 9999999 # penalizing unnecessary vehicles while maintaining the feasibility
    ):
        self.vehicle_capacity = vehicle_capacity
        self.vehicle_fixed_cost = vehicle_fixed_cost

    def solve_cluster(
            self,
            cluster_df
    ):
        """ A dynamic fleet number with a fixed fleet capacity """

        # Creating artificial depot (cluster centroid)
        depot_lat = cluster_df['Latitude'].mean()
        depot_lon = cluster_df['Longitude'].mean()
        
        depot_row = {
            'Latitude': depot_lat,
            'Longitude': depot_lon,
            'Demand_Forecast': 0
        }

        cluster_df = cluster_df.copy().reset_index(drop=True)

        cluster_df = pd.concat(
            [cluster_df, pd.DataFrame([depot_row])],
            ignore_index=True
        )

        # Depot index is the last index
        depot_index = len(cluster_df) - 1        
        
        demands = cluster_df['Demand_Forecast'].tolist()
        total_demand = sum(demands)

        # Feasibility check
        max_demand = max(demands)
        if max_demand > self.vehicle_capacity:
            print(f"Infeasible capacity: max demand {max_demand} exceeds the fixed vehicle capacity {self.vehicle_capacity}")
            return None

        # Dynamic vehicle count with tight vehicle count (No Slack!)
        base_vehicles = math.ceil(
            total_demand / self.vehicle_capacity
        )

        num_vehicles = math.ceil(base_vehicles * 1.05)
        
        # safety limit on vehicle numbers
        num_vehicles = min(
            num_vehicles,
            len(cluster_df) -1
        )

        print(f"Total cluster demand: {total_demand}")
        print(f"Vehicles used (no slack): {num_vehicles}")

        matrix_builder = DistanceMatrix()
        distance_matrix = matrix_builder.build(cluster_df)

        # RoutingIndexManager manager(10, 4, starts_ends)
        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix),
            num_vehicles,
            depot_index
        )

        routing = pywrapcp.RoutingModel(manager) 

        # distance callback
        def distance_callback(
                from_index,
                to_index
        ):
            
            from_node = manager.IndexToNode(int(from_index))
            to_node = manager.IndexToNode(int(to_index))
            return int(distance_matrix[from_node][to_node])
        
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Adding fixed cost of vehicles -> penalty
        for v in range(num_vehicles):
            routing.SetFixedCostOfVehicle(cost=self.vehicle_fixed_cost, vehicle=v)

        # Capacity constraint
        def demand_callback(
                from_index
        ):
            
            from_node = manager.IndexToNode(int(from_index))
            return demands[from_node]
        
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

        # def AddDimensionWithVehicleCapacity(self, evaluator_index: "int", slack_max: "int64", vehicle_capacities: "std::vector< int64 >", fix_start_cumul_to_zero: "bool", name: "std::string const &") -> "bool":
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,
            [self.vehicle_capacity] * num_vehicles,
            True,
            "Capacity"
        )

        # Search parameters
        search_params = pywrapcp.DefaultRoutingSearchParameters()
        search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        search_params.time_limit.seconds = 60 # Hard stop - 60 secs per cluster

        solution = routing.SolveWithParameters(search_params)

        if solution:
            return self._extract_routes(
                solution,
                routing,
                manager,
                num_vehicles
            )
        else:
            print("No feasible solution found within time limit!")
            return None
        
    def _extract_routes(
            self,
            solution,
            routing,
            manager,
            num_vehicles
    ):
        
        routes_data = []
        total_distance = 0
        total_load = 0

        capacity_dimension = routing.GetDimensionOrDie('Capacity')

        vehicles_in_use = 0

        for vehicle_id in range(num_vehicles):

            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)

                previous_index = index
                index = solution.Value(routing.NextVar(index))

                route_distance += routing.GetArcCostForVehicle(
                    previous_index,
                    index,
                    vehicle_id
                )
            
            # Compute route load
            route_load = solution.Value(
                capacity_dimension.CumulVar(previous_index)
            )

            if route_load > 0: 

                vehicles_in_use += 1

                utilization = 100 * (
                    route_load / self.vehicle_capacity
                )

                routes_data.append({
                    "vehicle_id": vehicle_id,
                    "stops": route,
                    "distance": route_distance,
                    "load": route_load,
                    "utilization_%": round(utilization, 2)
                })

                total_distance += route_distance
                total_load += route_load
        
        fleet_utilization = 100 * (
            total_load / (vehicles_in_use * self.vehicle_capacity)
        )

        print(f"\nVehicles in Use: {vehicles_in_use}")
        print(f"Cluster Total Distance: {total_distance}")
        print(f"Fleet Utilization: {round(fleet_utilization, 2)}%\n")

        return routes_data
