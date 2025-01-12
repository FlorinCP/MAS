import osmnx as ox
import random
from datetime import datetime
import os
import json

# Configuración
city_name = "Zaragoza, Spain"
graph_filename = "zaragoza_graph.graphml"

# Cargar o guardar el grafo
def load_or_save_zaragoza_graph(filename):
    if os.path.exists(filename):
        print(f"Loading graph from {filename}...")
        graph = ox.load_graphml(filename)
    else:
        print(f"Downloading graph for {city_name}...")
        graph = ox.graph_from_place(city_name, network_type="drive")
        ox.save_graphml(graph, filename)
        print(f"Graph saved to {filename}")
    return graph


# Generar el informe en formato JSON
def generate_json_emergency_report(graph) -> dict:
    import networkx as nx

    # Verifica si el grafo tiene nodos
    if nx.is_empty(graph):
        raise ValueError("The graph is empty. Cannot generate an emergency report.")

    # Selecciona un nodo aleatorio como ubicación
    location = random.choice(list(graph.nodes))
    location_coords = (graph.nodes[location]['y'], graph.nodes[location]['x'])

    # Generar ID único para el incidente
    incident_id = f"{random.randint(1000, 9999)}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generar detalles para la sección Médica
    injured_people = random.randint(1, 5)
    medical_details = []
    for _ in range(injured_people):
        medical_severity = random.randint(1, 10)
        injuries = random.sample(["Burns", "Fractures", "Lacerations", "Smoke Inhalation"], k=random.randint(1, 3))
        medical_details.append({
            'severity': medical_severity,
            'injuries': injuries
        })

    # Generar detalles para la sección de Bomberos
    fire_details = {
        'fire_level': random.choice(["Low", "Medium", "High"]),
        'affected_area': round(random.uniform(50, 5000), 2),
        'buildings_involved': random.randint(1, 10),
        'wind_direction': random.choice(["North", "South", "East", "West"]),
        'wind_speed': random.randint(10, 50),  # Wind speed in km/h
        'people_rescued': random.randint(1, 20),
        'fire_nature': random.choice(["Ordinary", "Electrical", "Gas", "Chemical"]),
        'building_level': random.choice(["Street level", "1st floor", "2nd floor", "Top floor"]),
    }

    # Generar detalles para la sección Policial
    police_details = {
        'situation_description': random.choice(["Armed robbery", "Hostage situation", "Protest", "Traffic accident"]),
        'suspects': random.randint(0, 5),
        'traffic_status': random.choice(["Clear", "Heavy Traffic", "Blocked"]),
        'crowd_size': random.randint(10, 500),
    }

    # Construir el informe en formato JSON
    json_report = {
        "incident_information": {
            "incident_id": incident_id,
            "timestamp": timestamp,
            "location": {
                "coordinates": location_coords,
                "node_id": location
            }
        },
        "medical_crew": {
            "injured_people": injured_people,
            "details": medical_details
        },
        "fire_crew": fire_details,
        "police_crew": police_details
    }

    return json_report


# Guardar el informe en un archivo .json
def save_report_to_json(report: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)
    print(f"Report saved to {filename}")


# Cargar el grafo y generar el informe
if __name__ == "__main__":
    graph = load_or_save_zaragoza_graph(graph_filename)
    if graph:
        report = generate_json_emergency_report(graph)
        filename = "emergency_report.json"
        save_report_to_json(report, filename)
