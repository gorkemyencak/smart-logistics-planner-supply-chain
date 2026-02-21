import folium
import random
from pathlib import Path

class GlobalVisualizer:

    @staticmethod
    def _random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def build(
        all_clusters_routes,
        save_path = "data/outputs/maps/global_map.html"
    ):
        
        if not all_clusters_routes:
            raise ValueError("No cluster route is provided!")
        
        # first coordinate to center map
        first_coord = None
        for cluster in all_clusters_routes:
            if not cluster:
                continue

            for route in cluster:
                geometry = route.get('geometry')

                if geometry:
                    first_coord = geometry[0]
                    break
            
            if first_coord:
                break
        
        if first_coord is None:
            raise ValueError('Routes contain no geometry!')
        
        m = folium.Map(
            location = first_coord,
            zoom_start = 10
        )

        for cluster_id, routes in enumerate(all_clusters_routes):
            if not routes:
                continue

            color = GlobalVisualizer._random_color()

            for route in routes:

                folium.PolyLine(
                    locations = route['geometry'],
                    color = color,
                    weight = 4,
                    opacity = 0.8,
                    tooltip = f"Cluster {cluster_id} | Vehicle {route['vehicle_id']}"
                ).add_to(m)
            
        Path(save_path).parent.mkdir(parents = True, exist_ok = True)
        m.save(save_path)

        print(f"Global map saved to {save_path}")
        return m