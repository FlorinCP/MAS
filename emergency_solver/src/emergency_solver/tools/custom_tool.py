from crewai.tools import BaseTool
from typing import Type, Tuple
from pydantic import BaseModel, Field
import json
import osmnx as ox
from emergency_solver.src.emergency_solver.schemas.schemas import RouteDistanceSchema, GeneralIncidenceReport, \
    IncidencePoliceReport, IncidenceFireReport, IncidenceMedicalReport
import networkx

from crewai.tools import BaseTool
from typing import Optional, Type

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class ComputeDistance(BaseTool):
    name: str = "Distance computation"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

class ReadEmergencyReport(BaseTool):
    name: str = "Emergency report reader"
    description: str = (
        "Tool that allows to read the initial Emergency report by the Dispatcher in MD format. It requires the path of the emergency report file."
    )

    def _run(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

class CraftGeneralIncidenceReport(BaseTool):
    name: str = "General incidence report"
    description: str = (
        "Tool that allows generating the GeneralIncidenceReport based on the information obtained from the emergency report."
        "It receives the emergency report as a dictionary and returns a GeneralIncidenceReport instance with the parsed medical,"
        "fire and police information."
    )

    def _run(self, emergency_report: dict) -> GeneralIncidenceReport:
        """
        Generates a GeneralIncidenceReport based on the provided emergency report.

        Args:
            emergency_report (dict): A dictionary containing detailed information about the emergency.

        Returns:
            GeneralIncidenceReport: An instance of the GeneralIncidenceReport with the populated data.
        """
        general = GeneralIncidenceReport()
        location = emergency_report["incident_information"]["location"]
        coordinates = location["coordinates"]  # Extract the list
        x: float = coordinates[0]
        y: float = coordinates[1]  # Ensure it's a tuple of floats
        coordinates = (x, y)
        # Parse and populate medical report if present
        if "medical_crew" in emergency_report:
            medical_crew = emergency_report["medical_crew"]
            general.medical = IncidenceMedicalReport(
                emergency_id=emergency_report["incident_information"]["incident_id"],
                coordinates=coordinates,
                node_id= location["node_id"],
                date=emergency_report["incident_information"]["timestamp"],
                injured_people=medical_crew["injured_people"],
                severity=max(d["severity"] for d in medical_crew["details"]),  # Use max severity from details
                dest_hospital="Hospital A",  # Placeholder destination hospital
                dist_to_hospital=5.0  # Placeholder distance in kilometers
            )

        # Parse and populate fire report if present
        if "fire_crew" in emergency_report:
            fire_crew = emergency_report["fire_crew"]
            general.fire = IncidenceFireReport(
                emergency_id=emergency_report["incident_information"]["incident_id"],
                coordinates=coordinates,
                node_id=location["node_id"],
                date=emergency_report["incident_information"]["timestamp"],
                fire_type=fire_crew["fire_nature"],
                severity=fire_crew["fire_level"].lower(),  # Assuming severity is mapped to fire level
                wind_direction=fire_crew["wind_direction"],
                wind_speed=fire_crew["wind_speed"],
                affected_area=fire_crew["affected_area"],
                people_to_rescue=fire_crew["people_rescued"],
                required_equipment=["Fire truck", "Ladder", "Extinguisher"]  # Placeholder equipment
            )

        # Parse and populate police report if present
        if "police_crew" in emergency_report:
            police_crew = emergency_report["police_crew"]
            general.police = IncidencePoliceReport(
                emergency_id=emergency_report["incident_information"]["incident_id"],
                coordinates=coordinates,
                node_id=location["node_id"],
                date=emergency_report["incident_information"]["timestamp"],
                affected_streets=[],  # Placeholder as street details are not provided
                traffic_status=police_crew["traffic_status"],
                crowd_size=police_crew["crowd_size"]
            )

        return general.json()


class ReadResources(BaseTool):
    name: str = "Resource file reader"
    description: str = (
        "Tool that allows to read the available resources from a JSON file."
    )

    def _run(self, file_name: str) -> str:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)



class RouteDistanceTool(BaseTool):
    name: str = 'Route distance calculator'
    description: str = 'A tool to find the driving route distance between an origin and a destination in a map given their coordinates.'
    args_schema: Type[BaseModel] = RouteDistanceSchema
    city_map: networkx.classes.multidigraph.MultiDiGraph = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, city_map: str, **kwargs):
        super().__init__(**kwargs)
        if not city_map:
            raise Exception('A valid city map path to a graphml file must be provided.')
        self.city_map = ox.load_graphml(city_map)
        self.city_map = ox.routing.add_edge_speeds(self.city_map)
        self.city_map = ox.routing.add_edge_travel_times(self.city_map)

    def _run(self, *args, **kwargs) -> int:
        args = args[0]
        x_origin = args.get('x_origin')
        y_origin = args.get('y_origin')
        x_destination = args.get('x_destination')
        y_destination = args.get('y_destination')

        return self._find_distance(x_origin, y_origin, x_destination, y_destination)

    def _find_distance(self, x_origin: float, y_origin: float, x_destination: float, y_destination: float) -> int:
        origin_node = ox.distance.nearest_nodes(self.city_map, X=x_origin, Y=y_origin)
        destination_node = ox.distance.nearest_nodes(self.city_map, X=x_destination, Y=y_destination)
        route = ox.shortest_path(self.city_map, origin_node, destination_node, weight='travel_time')
        edge_lengths = ox.routing.route_to_gdf(self.city_map, route)['length']

        return round(sum(edge_lengths))