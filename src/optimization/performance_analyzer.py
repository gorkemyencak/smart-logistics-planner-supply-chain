import numpy as np

class PerformanceAnalyzer:

    @staticmethod
    def analyze_cluster(routes):

        utilizations = [r["utilization_%"] for r in routes]
        loads = [r.get("load", 0) for r in routes]
        distances = [r.get("distance", 0) for r in routes]

        avg_utilization = float(np.mean(utilizations))
        min_utilization = float(np.min(utilizations))
        max_utilization = float(np.max(utilizations))
        std_utilization = float(np.std(utilizations))

        under_50 = [r for r in routes if r["utilization_%"] < 50]

        total_load = float(np.sum(loads))
        total_distance = float(np.sum(distances))
        n_routes = int(len(routes))

        print("-- Cluster Efficiency Report --")
        print(f"Avg Utilization: {round(avg_utilization, 2)}%")
        print(f"Min Utilization: {round(min_utilization, 2)}%")
        print(f"Max Utilization: {round(max_utilization, 2)}%")
        print(f"Std Dev Utilization: {round(std_utilization, 2)}%")
        print(f"Nb of Vehicles below 50% load: {len(under_50)}")
        print(f"Total Load Delivered: {round(total_load, 2)}")
        print(f"Total Distance: {round(total_distance, 2)}")
        print("--------------------------\n")

        return {
            "n_routes": n_routes,
            "avg": avg_utilization,
            "min": min_utilization,
            "max": max_utilization,
            "std": std_utilization,
            "under_50_count": len(under_50),
            "total_load": total_load,
            "total_distance": total_distance
        }