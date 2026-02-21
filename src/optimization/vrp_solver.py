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

    ### Vehicle Reduction Wrapper
    def solve_with_vehicle_reduction(
            self, 
            cluster_df: pd.DataFrame
    ):
        
        """ Iteratively reduce the vehicle count to find the minium feasible fleet size """

        cluster_df = cluster_df.copy().reset_index(drop=True)

        total_demand = cluster_df['Demand_Forecast'].sum()
        min_vehicles = math.ceil(
            total_demand / self.vehicle_capacity
        )

        # Start slightly above theoretical lower bound
        current_vehicles = min_vehicles + 2

        # Safety limit on current vehicle number
        current_vehicles = min(current_vehicles, len(cluster_df) - 1)    

        best_solution = None
        best_vehicle_count = None

        print(f"\nTotal cluster demand: {total_demand}")
        print(f"Theoretical lower bound on number of vehicles: {min_vehicles}")

        while current_vehicles >= min_vehicles:

            print(f"\nTrying to find a feasible solution with {current_vehicles} vehicles..")

            result = self._solve_once(
                cluster_df = cluster_df,
                num_vehicles = current_vehicles
            )

            if result['feasible']:
                print(f"Feasible with {current_vehicles} vehicles..")

                best_solution = result['routes']
                best_vehicle_count = current_vehicles

                current_vehicles -= 1
            else:
                print(f"Infeasible with {current_vehicles} vehicles!")
                break
        
        print(f"\nFinal selected vehicle count: {best_vehicle_count}\n")

        return best_solution
    
    ### Single Solve Attempt for a Fixed Vehicle Count per Cluster
    def _solve_once(
            self,
            cluster_df: pd.DataFrame,
            num_vehicles: int
    ):
        
        """ Solving VRP per cluster for a fixed vehicle count """
        # Creating artificial depot (cluster centroid)
        depot_lat = cluster_df['Latitude'].mean()
        depot_lon = cluster_df['Longitude'].mean()

        depot_row = {
            'Latitude': depot_lat,
            'Longitude': depot_lon,
            'Demand_Forecast': 0,
            'Traffic_Status': 'Clear',
            'Waiting_Time': 0,
            'Traffic_Encoded': 1,
            'Cluster_ID': -1
        }

        cluster_df = cluster_df.copy().reset_index(drop=True)

        cluster_df = pd.concat(
            [cluster_df, pd.DataFrame([depot_row])],
            ignore_index = True
        )

        # Depot index is the last index
        depot_index = len(cluster_df) - 1

        demands = cluster_df['Demand_Forecast'].tolist()
        total_demand = sum(demands)

        # Feasibility check
        max_demand = max(demands)
        if max_demand > self.vehicle_capacity:
            print(f"Infeasible capacity: max demand {max_demand} exceeds the fixed vehicle capacity {self.vehicle_capacity}")
            return {'feasible': False}
        
        # Distance matrix
        matrix_builder = DistanceMatrix()
        distance_matrix = matrix_builder.build(cluster_df)

        # OR-Tools Model
        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix),
            num_vehicles,
            depot_index
        )

        routing = pywrapcp.RoutingModel(manager)

        # Distance callback
        def distance_callback(
                from_index,
                to_index
        ):
            try:
                from_index = int(from_index)
                to_index = int(to_index)

                if from_index < 0 or to_index <0:
                    return 0
                
                if from_index >= manager.GetNumberOfIndices() or to_index >= manager.GetNumberOfIndices():
                    return 0
                
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)

                return int(distance_matrix[from_node][to_node])

            except Exception:
                return 0


        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Adding fixed cost of vehicles -> penalty
        for v in range(num_vehicles):
            routing.SetFixedCostOfVehicle(cost = self.vehicle_fixed_cost, vehicle = v)
        
        # Capacity constraint
        def demand_callback(from_index):
            
            try:
                from_index = int(from_index)

                if from_index < 0 or from_index >= manager.GetNumberOfIndices():
                    return 0 
                
                from_node = manager.IndexToNode(from_index)

                return demands[from_node]

            except Exception:
                return 0
        
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

        routing.AddDimensionWithVehicleCapacity(
            evaluator_index = demand_callback_index,
            slack_max = 0,
            vehicle_capacities = [self.vehicle_capacity] * num_vehicles,
            fix_start_cumul_to_zero = True,
            name = 'Capacity'
        )

        # Search parameters
        search_params = pywrapcp.DefaultRoutingSearchParameters()
        search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        search_params.time_limit.seconds = 30 # Hard stop - 30 secs per cluster

        solution = routing.SolveWithParameters(search_parameters = search_params)

        if solution:
            routes = self._extract_routes(
                solution,
                routing,
                manager,
                num_vehicles,
                demands,
                cluster_df
            )

            return {
                'feasible': True,
                'routes': routes
            }
        else:
            print("No feasible solution found within time limit!")
            return {'feasible': False}
        
        
    ### Route Extraction
    def _extract_routes(
            self,
            solution,
            routing,
            manager,
            num_vehicles,
            demands,
            cluster_df
    ):
        
        routes_data = []
        total_distance = 0
        total_load = 0
        vehicles_in_use = 0

        for vehicle_id in range(num_vehicles):

            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0
            route_load = 0

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)

                route_load += demands[node]

                previous_index = index
                index = solution.Value(routing.NextVar(index))

                route_distance += routing.GetArcCostForVehicle(
                    from_index = previous_index,
                    to_index = index,
                    vehicle = vehicle_id
                )

            if route_load > 0:
                
                vehicles_in_use += 1
                utilization = 100 * (route_load / self.vehicle_capacity)

                # building geometry from route nodes
                geometry = []

                for node_idx in route:
                    if node_idx >= len(cluster_df):
                        continue

                    row = cluster_df.iloc[node_idx]
                    geometry.append((row['Latitude'], row['Longitude']))

                routes_data.append({
                    'vehicle_id': vehicle_id,
                    'stops': route,
                    'distance': route_distance,
                    'load': route_load,
                    'utilization_%': round(utilization, 2),
                    'geometry': geometry
                })

                total_distance += route_distance
                total_load += route_load

        fleet_utilization = 0
        if vehicles_in_use > 0:
            fleet_utilization = 100 * (total_load / (self.vehicle_capacity * vehicles_in_use))
        
        print(f"Vehicles in Use: {vehicles_in_use}")
        print(f"Cluster Total Distance: {total_distance}")
        print(f"Fleet Utilization: {round(fleet_utilization, 2)}%\n")

        return routes_data             

