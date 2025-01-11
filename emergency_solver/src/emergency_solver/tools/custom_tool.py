from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
import json
import osmnx as ox
from src.emergency_solver.schemas.schemas import RouteDistanceSchema, GeneralIncidenceReport, \
    IncidencePoliceReport, IncidenceFireReport, IncidenceMedicalReport
import networkx

from crewai_tools import BaseTool
from typing import Optional, Type

from src.emergency_solver.utils.report_parser import EmergencyReportParser

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


from crewai.tools import BaseTool
from typing import Dict, Any
from datetime import datetime
from src.emergency_solver.schemas.schemas import (
    GeneralIncidenceReport,
    IncidenceMedicalReport,
    IncidenceFireReport,
    IncidencePoliceReport
)


class ReadEmergencyReport(BaseTool):
    name: str = "Emergency report reader"
    description: str = "Tool that reads the initial Emergency report in MD format."

    def _run(self, path: str) -> str:
        """
        Simply reads the emergency report file and returns its contents.
        The parsing will be done by the CraftGeneralIncidenceReport tool.
        """
        with open(path, "r", encoding="utf-8") as file:
            return file.read()


class CraftGeneralIncidenceReport(BaseTool):
    name: str = "General incidence report"
    description: str = (
        "Tool that allows generating the GeneralIncidenceReport based on the information "
        "obtained from the emergency report."
    )

    def parse_markdown_to_dict(self, markdown_content: str) -> Dict[str, Any]:
        """
        Converts markdown formatted emergency report into a structured dictionary.
        """
        sections = {}
        current_section = None
        section_data = {}

        for line in markdown_content.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Handle section headers (e.g., "## Incident Information")
            if line.startswith('## '):
                if current_section and section_data:
                    sections[current_section] = section_data
                current_section = line.strip('# ')
                section_data = {}

            # Handle data lines (e.g., "- **Incident ID:** 2855")
            elif line.startswith('- **') and current_section:
                try:
                    # Split the line into key and value
                    key_value = line.strip('- **').split(':**')
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        value = key_value[1].strip()
                        section_data[key] = value
                except Exception as e:
                    print(f"Error parsing line '{line}': {str(e)}")

        # Add the last section
        if current_section and section_data:
            sections[current_section] = section_data

        return sections

    def _run(self, emergency_report: str) -> GeneralIncidenceReport:
        """
        Creates a GeneralIncidenceReport from the markdown emergency report.
        """
        try:
            # First parse the markdown into a structured dictionary
            parsed_data = self.parse_markdown_to_dict(emergency_report)

            # Extract core information
            incident_info = parsed_data.get('Incident Information', {})
            incident_id = int(incident_info.get('Incident ID', 0))
            timestamp = incident_info.get('Timestamp', '')
            location = incident_info.get('Location', '')

            # Create date object
            date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

            # Process Medical Report
            medical_report = None
            if medical_data := parsed_data.get('Medical Crew'):
                medical_report = IncidenceMedicalReport(
                    emergency_id=incident_id,
                    location=str(location),  # Ensure location is string
                    date=date,
                    injured_people=int(medical_data.get('Number of Injured People', 0)),
                    severity='medium',  # Default severity
                    dest_hospital='TBD',  # To be determined
                    dist_to_hospital=0.0  # To be calculated
                )

            # Process Fire Report
            fire_report = None
            if fire_data := parsed_data.get('Fire Crew'):
                fire_report = IncidenceFireReport(
                    emergency_id=incident_id,
                    location=str(location),
                    date=date,
                    fire_type=fire_data.get('Fire Nature', 'unknown'),
                    severity=fire_data.get('Fire Level (1-5)', 'low'),
                    wind_direction=fire_data.get('Wind Direction', 'unknown'),
                    wind_speed=int(fire_data.get('Wind Speed (km/h)', 0)),
                    affected_area=float(fire_data.get('Affected Area (m²)', 0)),
                    people_to_rescue=int(fire_data.get('People Needing Rescue', 0)),
                    required_equipment=['Fire truck', 'Ladder', 'Extinguisher']
                )

            # Process Police Report
            police_report = None
            if police_data := parsed_data.get('Police Crew'):
                police_report = IncidencePoliceReport(
                    emergency_id=incident_id,
                    location=str(location),
                    date=date,
                    affected_streets=[],  # To be determined by police
                    traffic_status=police_data.get('Traffic Status', 'unknown'),
                    crowd_size=int(police_data.get('Crowd Size', 0))
                )

            # Create and return the complete report
            return GeneralIncidenceReport(
                medical=medical_report,
                fire=fire_report,
                police=police_report
            )

        except Exception as e:
            print(f"Error creating general incidence report: {str(e)}")
            raise
