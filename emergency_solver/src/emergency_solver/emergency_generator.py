import osmnx as ox
import random
from datetime import datetime
import os

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


# Generar el informe en formato markdown
def generate_markdown_emergency_report_with_map(graph) -> str:
    import networkx as nx

    # Verifica si el grafo tiene nodos
    if nx.is_empty(graph):
        raise ValueError("The graph is empty. Cannot generate an emergency report.")

    # Selecciona un nodo aleatorio como ubicación
    location = random.choice(list(graph.nodes))
    location_coords = (graph.nodes[location]['y'], graph.nodes[location]['x'])

    # Generar ID único para el incidente
    incident_id = f"INC-{random.randint(1000, 9999)}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generar detalles para la sección Médica
    injured_people = random.randint(1, 5)
    medical_details = []
    for _ in range(injured_people):
        medical_severity = random.randint(1, 10)
        injuries = ", ".join(random.sample(["Burns", "Fractures", "Lacerations", "Smoke Inhalation"], k=random.randint(1, 3)))
        medical_details.append({
            'severity': medical_severity,
            'injuries': injuries
        })

    # Generar detalles para la sección de Bomberos
    fire_level = random.choice(["Low", "Medium", "High"])
    affected_area = round(random.uniform(50, 5000), 2)
    buildings_involved = random.randint(1, 10)
    wind_direction = random.choice(["North", "South", "East", "West"])
    wind_speed = random.randint(10, 50)  # Wind speed in km/h
    people_rescued = random.randint(1, 20)
    fire_nature = random.choice(["Ordinary", "Electrical", "Gas", "Chemical"])
    building_level = random.choice(["Street level", "1st floor", "2nd floor", "Top floor"])

    # Generar detalles para la sección Policial
    police_description = random.choice(["Armed robbery", "Hostage situation", "Protest", "Traffic accident"])
    suspects = random.randint(0, 5)
    traffic_status = random.choice(["Clear", "Heavy Traffic", "Blocked"])
    crowd_size = random.randint(10, 500)

    # Construir el informe en formato markdown
    markdown_report = f"""
# Emergency Report

## Incident Information
- **Incident ID:** {incident_id}
- **Timestamp:** {timestamp}
- **Location:** Coordinates {location_coords} (Node ID: {location})

## Medical Crew
- **Number of Injured People:** {injured_people}
- {''.join([f"**Injured Person {i+1}:** Severity: {medical_details[i]['severity']}, Injuries: {medical_details[i]['injuries']}\n" for i in range(injured_people)])}

## Fire Crew
- **Fire Level (1-5):** {fire_level}
- **Affected Area (m²):** {affected_area}
- **Buildings Involved:** {buildings_involved}
- **Wind Direction:** {wind_direction}
- **Wind Speed (km/h):** {wind_speed}
- **People Needing Rescue:** {people_rescued}
- **Fire Nature:** {fire_nature}
- **Building Level:** {building_level}

## Police Crew
- **Situation Description:** {police_description}
- **Number of Suspects:** {suspects}
- **Traffic Status:** {traffic_status}
- **Crowd Size:** {crowd_size}
    """

    return markdown_report.strip()


# Guardar el informe en un archivo .md
def save_report_to_file(report: str, filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)
    print(f"Report saved to {filename}")

# Cargar el grafo y generar el informe
if __name__ == "__main__":
    graph = load_or_save_zaragoza_graph(graph_filename)
    if graph:
        report = generate_markdown_emergency_report_with_map(graph)
        filename = f"emergency_report_{datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')}.md"
        save_report_to_file(report, filename)
