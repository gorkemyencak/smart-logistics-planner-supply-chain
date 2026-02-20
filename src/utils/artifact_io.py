import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def _resolve_dir(
        output_dir: str
):
    return PROJECT_ROOT / output_dir

def save_cluster_artifact(
        cluster_id,
        routes,
        metrics,
        solver_meta = None,
        output_dir = "data/outputs/artifacts"
):
    
    """ Saving full VRP artifact (routes & metadata) """
    output_dir = _resolve_dir(output_dir)
    os.makedirs(output_dir, exist_ok = True)

    artifact = {
        'cluster_id': int(cluster_id),
        'routes': routes,
        'metrics': metrics,
        'solver_meta': solver_meta or {}
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

def load_cluster_artifact(
        cluster_id,
        output_dir = "data/outputs/artifacts"
):
    
    output_dir = _resolve_dir(output_dir)
    path = output_dir / f"cluster_{cluster_id}_artifact.json"

    try:
        with open(path) as f:
            artifact = json.load(f)

        return artifact
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Artifact not found on: {path}")
