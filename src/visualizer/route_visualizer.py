import folium
import random
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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
        
        output_dir = PROJECT_ROOT / output_dir
        os.makedirs(output_dir, exist_ok = True)
        
        # Center map at depot
        m = folium.Map(
            location = [self.depot_lat, self.depot_lon],
            zoom_start = 6,
            tiles = "OpenStreetMap"
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
        file_path = output_dir / f"cluster_{cluster_id}_routes.html" 
        m.save(str(file_path))

        print(f"Map saved to {file_path}")

        return m, str(file_path)
    
    def save_static_image(
            self,
            html_path,
            output_path = None,
            wait_seconds = 3
    ):
        """ Save a PNG snapshot of a folium map """
        html_path = Path(html_path)

        if output_path is None:
            output_path = html_path.with_suffix(".png")
        else:
            output_path = Path(output_path)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1400,900")

        driver = webdriver.Chrome(
            service = Service(ChromeDriverManager().install()),
            options = options
        )

        driver.get(f"file://{html_path.resolve()}")

        time.sleep(wait_seconds)

        driver.save_screenshot(str(output_path))
        driver.quit()

        # removing browser padding
        img = Image.open(str(output_path))
        img.save(str(output_path))

        print(f"Static image saved to {output_path}")
        return str(output_path)

