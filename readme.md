## Smart Logistics Planner

End-to-end $\textbf{\textit{Capacitated Vehicle Routing Optimization (CVRP)}}$ project that simulates how logistics companes plan deliveries efficiently using clustering, OR-Tools, and interactive map visualization.

## Problem Statement

Logistics companies must assign deliveries to vehicles while minimizing travel distance and maximizing vehicle utilization.

This project solves:
* Capacitated Vehicle Routing Problem (CVRP)
* Performance evaluation of generated routes
* Visual inspection of optimization quality

## How to Run

    pip install -r requirements.txt
    python main.py

Then open notebooks to explore results.

## Metrics
The project evaluates routing quality using:
* Average vehicle utilization
* Min/Max utilization
* Standard deviation of utilization
* Under-utilized vehicle count

## Visualization
### Cluster Map
Shows vehicle routes for a single cluster.

### Global Map
Shows all cluster together with color separation.

## Artifacts
Route artifacts contain:
* vehicle routes
* geometry (coordinates)
* utilization
* metadata

## Output

* Per-cluster route maps
* Global map across all clusters
* Vehicle utilization metrics
* Saved routing artifacts