import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def _resolve_dir(
        output_dir: str
):
    return PROJECT_ROOT / output_dir


def save_routes(
        routes,
        cluster_id,
        output_dir = "data/outputs/routes"
):
    
    output_dir = _resolve_dir(output_dir)
    os.makedirs(output_dir, exist_ok = True)

    path = f"{output_dir}/cluster_{cluster_id}_routes.json"

    with open(path, 'w') as f:
        json.dump(
            routes,
            f,
            indent = 2
        )
    
    print(f"Routes saved to {path}")
    return path

def load_routes(
        cluster_id,
        output_dir = "data/outputs/routes"
):
    
    output_dir = _resolve_dir(output_dir)
    path = f"{output_dir}/cluster_{cluster_id}_routes.json"

    try: 
        with open(path, 'r') as f:
            routes = json.load(f)
        return routes
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Routes not found: {path}")
    
