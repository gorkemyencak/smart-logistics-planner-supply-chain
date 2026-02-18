from src.data.kaggle_loader import KaggleCSVLoader
from src.data.data_validator import DataValidator
from src.data.data_preprocessor import DataPreprocessor
from src.optimization.vrp_solver import VRPsolver
from src.optimization.performance_analyzer import PerformanceAnalyzer
from src.clustering.demand_aware_clusterer import DemandAwareClusterer

def main(): 
    loader = KaggleCSVLoader(
        dataset_name = "ziya07/smart-logistics-supply-chain-dataset"
    )

    # Downloading the dataset from Kaggle into local directory
    loader.download_dataset()

    # Loading the local dataset from local directory
    df = loader.load_local_csv("smart_logistics_dataset.csv")

    # Data Overview
    loader.data_overview(df)

    # Validating the Dataset
    dataset_columns = df.columns.tolist()

    validator = DataValidator(required_columns=dataset_columns)
    validator.validate_columns(df)
    validator.validate_missing_values(df)

    # Generic Preprocessing
    preprocessor = DataPreprocessor()
    df_clean = preprocessor.clean(df)
    df_clean = preprocessor.convert_datetime(df_clean, ['Timestamp'])

    routing_df = preprocessor.prepare_for_routing(df_clean)

    # Saving to processed folder
    preprocessor.save_processed(df_clean, "processed_smart_logistics_dataset.csv")

    # Node Clustering
    clusterer = DemandAwareClusterer(
        vehicle_capacity = 750,
        target_vehicles_per_cluster = 15
    )
    routing_df = clusterer.cluster(routing_df)

    print("\nCluster Distribution")
    print(routing_df['Cluster_ID'].value_counts().sort_index())

    # Solving VRP per Cluster
    solver = VRPsolver(vehicle_capacity = 750)

    for cluster_id in sorted(routing_df['Cluster_ID'].unique()):
        print(f"\n-- Solving Cluster {cluster_id} --")

        cluster_data = routing_df[
            routing_df['Cluster_ID'] == cluster_id
        ].reset_index(drop=True)

        routes = solver.solve_cluster(cluster_data)

        if routes:
            PerformanceAnalyzer.analyze_cluster(routes)

        print(f"Routes: {routes}")
    
if __name__ == '__main__':
    main()

    # phase 1: demand aware clustering
    # phase 2: smart vehicle allocation
    # phase 3: metaheuristic tuning
    # phase 4: cost modeling
    # phase 5: visualization dashboard