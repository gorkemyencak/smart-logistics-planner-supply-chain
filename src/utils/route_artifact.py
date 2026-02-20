import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def _resolve_dir(
        output_dir: str
):
    return PROJECT_ROOT / output_dir

def save_route_artifact(
        cluster_id,
        cluster_df,
        routes,
        metrics = None,
        output_dir = "data/outputs/artifacts"
):
    
    """ Saving full VRP artifact (routes & metadata) """
    output_dir = _resolve_dir(output_dir)
    os.makedirs(output_dir, exist_ok = True)

    artifact = {
        'cluster_id': int(cluster_id),
        'n_nodes': int(len(cluster_df)),
        'total_demand': float(cluster_df['Demand_Forecast'].sum()),
        'n_routes': int(len(routes)),
        'routes': routes,
        'metrics': metrics or {}
    }

    path = output_dir / f"cluster_{cluster_id}_artifact.json"

    with open(path, 'w') as f:
        json.dump(
            artifact,
            f,
            indent = 2
        )

    print(f"Artifact saved to {path}")
    return path

def load_route_artifact(
        cluster_id,
        output_dir = 'data/outputs/artifacts'
):
    
    output_dir = _resolve_dir(output_dir)
    path = output_dir / f"cluster_{cluster_id}_artifact.json"

    try:
        with open(path) as f:
            return json.load(f)
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Artifact not found on: {path}")
