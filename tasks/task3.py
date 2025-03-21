import csv
import networkx as nx
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import time

# Function to read NYC taxi data from a .txt file
def read_nyc_taxi_data(filepath):
    """
    Read taxi trip data from the given file and return a list of (pickup, dropoff) pairs.

    Args:
        filepath (str): Path to the NYC taxi dataset (.txt file)

    Returns:
        list: List of tuples containing pickup and dropoff location IDs.
    """
    taxi_data = []
    with open(filepath, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip the header row
        for row in reader:
            try:
                pickup = int(row[5]) if row[5].isdigit() else None  # Extract pickup location ID
                dropoff = int(row[6]) if row[6].isdigit() else None  # Extract dropoff location ID
                taxi_data.append((pickup, dropoff))  # Add pickup and dropoff pair to the list
            except (IndexError, ValueError):
                continue  # Skip rows with invalid data
    return taxi_data

# Function to read taxi zone lookup data from a CSV file
def read_taxi_zone_lookup(filepath):
    """
    Read taxi zone lookup data and return a dictionary mapping LocationIDs to Zone names.

    Args:
        filepath (str): Path to the taxi zone lookup CSV file

    Returns:
        dict: Mapping between LocationIDs and Zone names.
    """
    taxi_zone_lookup = {}
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            taxi_zone_lookup[int(row['LocationID'])] = row['Zone']
    return taxi_zone_lookup

# Function to build a graph using NetworkX from the taxi data
def build_graph(taxi_data, taxi_zone_lookup):
    """
    Build a graph representing taxi trips between pickup and dropoff locations.

    Args:
        taxi_data (list): List of (pickup, dropoff) pairs
        taxi_zone_lookup (dict): Mapping of LocationIDs to Zone names

    Returns:
        networkx.Graph: Graph object representing taxi trips.
    """
    graph = nx.Graph()
    trip_counts = defaultdict(int)

    # Add nodes to the graph with zone names
    for zone_id, zone_name in taxi_zone_lookup.items():
        graph.add_node(zone_id, name=zone_name)

    # Count the number of trips between pickup and dropoff pairs
    for pickup, dropoff in taxi_data:
        if pickup and dropoff:
            trip_counts[(pickup, dropoff)] += 1

    # Add edges to the graph with weights based on the number of trips
    for (pickup, dropoff), count in trip_counts.items():
        graph.add_edge(pickup, dropoff, weight=count)

    return graph

# Function to find connected components using NetworkX's built-in method
def find_connected_components_networkx(graph):
    """
    Find connected components in a graph using NetworkX's built-in function.

    Args:
        graph (networkx.Graph): Graph object

    Returns:
        list: List of sets containing nodes in each connected component.
    """
    return list(nx.connected_components(graph))

# Function to find connected components using DFS
def find_connected_components_dfs(graph):
    """
    Find connected components in a graph using Depth-First Search (DFS).

    Args:
        graph (networkx.Graph): Graph object

    Returns:
        list: List of lists containing nodes in each connected component.
    """
    visited = set()
    components = []

    def dfs(node):
        """
        Depth-First Search function to traverse and collect connected nodes.

        Args:
            node (int): Starting node

        Returns:
            list: List of nodes in the connected component.
        """
        stack = [node]
        component = []
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                component.append(current)
                stack.extend(set(graph.neighbors(current)) - visited)
        return component

    for node in graph.nodes:
        if node not in visited:
            components.append(dfs(node))

    return components

# Function to find connected components using BFS
def find_connected_components_bfs(graph):
    """
    Find connected components in a graph using Breadth-First Search (BFS).

    Args:
        graph (networkx.Graph): Graph object

    Returns:
        list: List of lists containing nodes in each connected component.
    """
    visited = set()
    components = []

    def bfs(node):
        """
        Breadth-First Search function to traverse and collect connected nodes.

        Args:
            node (int): Starting node

        Returns:
            list: List of nodes in the connected component.
        """
        queue = deque([node])
        component = []
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                component.append(current)
                queue.extend(set(graph.neighbors(current)) - visited)
        return component

    for node in graph.nodes:
        if node not in visited:
            components.append(bfs(node))

    return components

# Function to plot the graph using matplotlib
def plot_graph(graph, components=None):
    """
    Plot the graph using matplotlib and NetworkX.

    Args:
        graph (networkx.Graph): Graph object
        components (list, optional): List of sets containing nodes in each connected component
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=700)

    # Draw edges with varying widths based on the number of trips
    all_weights = [data['weight'] for (_, _, data) in graph.edges(data=True)]
    unique_weights = list(set(all_weights))
    for weight in unique_weights:
        weighted_edges = [(u, v) for (u, v, d) in graph.edges(data=True) if d['weight'] == weight]
        nx.draw_networkx_edges(graph, pos, edgelist=weighted_edges, width=weight * 0.1)

    # Draw node labels
    nx.draw_networkx_labels(graph, pos)

    plt.show()

# Function to compare the performance of NetworkX's connected component function with DFS and BFS
def compare_performance(graph):
    """
    Compare the performance of finding connected components using NetworkX's built-in method,
    DFS, and BFS.

    Args:
        graph (networkx.Graph): Graph object
    """
    # NetworkX
    start_time = time.time()
    networkx_components = find_connected_components_networkx(graph)
    networkx_time = time.time() - start_time

    # DFS
    start_time = time.time()
    dfs_components = find_connected_components_dfs(graph)
    dfs_time = time.time() - start_time

    # BFS
    start_time = time.time()
    bfs_components = find_connected_components_bfs(graph)
    bfs_time = time.time() - start_time

    print(f"NetworkX: {networkx_time:.4f} seconds, Components: {len(networkx_components)}")
    print(f"DFS: {dfs_time:.4f} seconds, Components: {len(dfs_components)}")
    print(f"BFS: {bfs_time:.4f} seconds, Components: {len(bfs_components)}")

# Main Execution
# Load taxi trip data foe all datasets
taxi_data_small = read_nyc_taxi_data('nyc_dataset_small.txt')
taxi_data_medium = read_nyc_taxi_data('nyc_dataset_medium.txt')
taxi_data_large = read_nyc_taxi_data('nyc_dataset_large.txt')

# Load taxi zone lookup data for all datasets
taxi_zone_lookup_small = read_taxi_zone_lookup('taxi+_zone_lookup.csv')
taxi_zone_lookup_medium = read_taxi_zone_lookup('taxi+_zone_lookup.csv')
taxi_zone_lookup_large = read_taxi_zone_lookup('taxi+_zone_lookup.csv')

# Build the graph from taxi data for all datasets
graph_small = build_graph(taxi_data_small, taxi_zone_lookup_small)
graph_medium = build_graph(taxi_data_medium, taxi_zone_lookup_medium)
graph_large = build_graph(taxi_data_large, taxi_zone_lookup_large)

# Find connected components using NetworkX for all datasets
components_small = find_connected_components_networkx(graph_small)
components_medium = find_connected_components_networkx(graph_medium)
components_large = find_connected_components_networkx(graph_large)

# Plot the graph
plot_graph(graph_small, components_small)
plot_graph(graph_medium, components_medium)
plot_graph(graph_large, components_large)

# Compare the performance of different connected component finding methods for all datasets
compare_performance(graph_small)
compare_performance(graph_medium)
compare_performance(graph_large)
