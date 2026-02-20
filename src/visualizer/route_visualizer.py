import folium
import random
import os

class RouteVisualizer:

    def __init__(
            self,
            depot_lat,
            depot_lon
    ):
        
        self.depot_lat = depot_lat
        self.depot_lon = depot_lon

    
    def _random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return f"#{r:02x}{g:02x}{b:02x}"
    
    def visualize_cluster_routes(
            self,
            cluster_df,
            routes,
            cluster_id,
            output_dir = "data/outputs/map"
    ):
        
        os.makedirs(output_dir, exist_ok = True)
        
        # Center map at depot
        m = folium.Map(
            location = [self.depot_lat, self.depot_lon],
            zoom_start = 6
        )

        # Mark depot
        folium.Marker(
            location = [self.depot_lat, self.depot_lon],
            popup = 'Depot',
            icon = folium.Icon(
                color = 'black',
                icon = 'home',
                icon_color = 'red'
            )
        ).add_to(m)

        # Plot demand nodes
        for idx, row in cluster_df.iterrows():

            # Skip depot
            if row['Demand_Forecast'] == 0:
                continue

            folium.CircleMarker(
                location = [row['Latitude'], row['Longitude']],
                radius = 4,
                color = 'blue',
                fill = True,
                fill_opacity = 0.6,
                popup = f"Demand: {row['Demand_Forecast']}"
            ).add_to(m)
        
        # Draw routes
        for route in routes:
            color = self._random_color()
            
            # Start at depot
            coordinates = [(self.depot_lat, self.depot_lon)]

            # Stops
            for stop_idx in route['stops']:

                if stop_idx >= len(cluster_df):
                    continue

                r = cluster_df.iloc[stop_idx]
                coordinates.append((r['Latitude'], r['Longitude']))
            
            coordinates.append((self.depot_lat, self.depot_lon))

            folium.PolyLine(
                locations = coordinates,
                color = color,
                weight = 3,
                opacity = 0.8,
                popup = f"Vehicle {route['vehicle_id']} | Load: {route['load']}"
            ).add_to(m)
        
        # Save
        file_path = os.path.join(output_dir, f"cluster_{cluster_id}_routes.html")
        m.save(file_path)

        print(f"Map saved to {file_path}")

        return m, os.path.abspath(file_path)
