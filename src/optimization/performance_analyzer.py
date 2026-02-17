import numpy as np

class PerformanceAnalyzer:

    @staticmethod
    def analyze_cluster(routes):

        utilizations = [r["utilization_%"] for r in routes]

        avg_utilization = np.mean(utilizations)
        min_utilization = np.min(utilizations)
        max_utilization = np.max(utilizations)
        std_utilization = np.std(utilizations)

        under_50 = [r for r in routes if r["utilization_%"] < 50]

        print("-- Cluster Efficiency Report --")
        print(f"Avg Utilization: {round(avg_utilization, 2)}%")
        print(f"Min Utilization: {round(min_utilization, 2)}%")
        print(f"Max Utilization: {round(max_utilization, 2)}%")
        print(f"Std Dev Utilization: {round(std_utilization, 2)}%")
        print(f"Nb of Vehicles below 50% load: {len(under_50)}")
        print("--------------------------\n")

        return {
            "avg": avg_utilization,
            "min": min_utilization,
            "max": max_utilization,
            "std": std_utilization,
            "under_50_count": len(under_50)
        }