from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import osmnx as ox
from emergency_solver.src.emergency_solver.schemas.schemas import RouteDistanceSchema, GeneralIncidenceReport, \
    IncidencePoliceReport, IncidenceFireReport, IncidenceMedicalReport
import networkx

from crewai_tools import BaseTool
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
        print(emergency_report)
        # Parse and populate medical report if present
        if "Medical Crew" in emergency_report:
            general.medical = IncidenceMedicalReport(
                emergency_id=emergency_report["Incident ID"],
                location=emergency_report["Location"],
                date=emergency_report["Timestamp"],
                injured_people=emergency_report["Medical Crew"]["Number of Injured People"],
                severity="high",  # Assuming severity from injuries provided
                dest_hospital="Hospital A",  # Placeholder destination hospital
                dist_to_hospital=5.0  # Placeholder distance in kilometers
            )

        # Parse and populate fire report if present
        if "Fire Crew" in emergency_report:
            general.fire = IncidenceFireReport(
                emergency_id=emergency_report["Incident ID"],
                location=emergency_report["Location"],
                date=emergency_report["Timestamp"],
                fire_type=emergency_report["Fire Crew"]["Fire Level (1-5)"],
                severity="medium",  # From fire level provided
                wind_direction=emergency_report["Fire Crew"]["Wind Direction"],
                wind_speed=emergency_report["Fire Crew"]["Wind Speed (km/h)"],
                affected_area=emergency_report["Fire Crew"]["Affected Area (m²)"],
                people_to_rescue=emergency_report["Fire Crew"]["People Needing Rescue"],
                required_equipment=["Fire truck", "Ladder", "Extinguisher"]  # Placeholder equipment
            )

        # Parse and populate police report if present
        if "Police Crew" in emergency_report:
            general.police = IncidencePoliceReport(
                emergency_id=emergency_report["Incident ID"],
                location=emergency_report["Location"],
                date=emergency_report["Timestamp"],
                affected_streets=[],  # No street details provided
                traffic_status=emergency_report["Police Crew"]["Traffic Status"],
                crowd_size=emergency_report["Police Crew"]["Crowd Size"]
            )

        return general


class ReadResources(BaseTool):
    name: str = "Resource file reader"
    description: str = (
        "Tool that allows to read the available resources from a JSON file."
    )

    def _run(self, argument: str) -> str:
        with open(argument, "r", encoding="utf-8") as file:
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