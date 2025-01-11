from typing import Dict, Any
from datetime import datetime

from crewai.tools import BaseTool

from src.emergency_solver.schemas.schemas import (
    GeneralIncidenceReport,
    IncidenceMedicalReport,
    IncidenceFireReport,
    IncidencePoliceReport
)


class EmergencyReportParser:
    """
    Parser for emergency reports that handles data validation and transformation.
    This class serves as a central point for processing incoming emergency data.
    """

    @staticmethod
    def parse_markdown_to_dict(markdown_content: str) -> Dict[str, Any]:
        """
        Convert markdown formatted emergency report into a structured dictionary.

        Args:
            markdown_content: Raw markdown string from the emergency report

        Returns:
            Dictionary containing parsed emergency data
        """
        sections = {}
        current_section = None
        current_subsection = None

        for line in markdown_content.split('\n'):
            line = line.strip()
            if not line:
                continue

            if line.startswith('## '):
                # Main section (e.g., "Incident Information")
                current_section = line.strip('# ')
                sections[current_section] = {}
                current_subsection = None
            elif line.startswith('- **'):
                # Key-value pair
                if ':**' in line:
                    key, value = line.split(':**', 1)
                    key = key.strip('- *')
                    value = value.strip()

                    if current_subsection:
                        if current_subsection not in sections[current_section]:
                            sections[current_section][current_subsection] = {}
                        sections[current_section][current_subsection][key] = value
                    else:
                        sections[current_section][key] = value

        return sections

    @classmethod
    def create_incidence_reports(cls, parsed_data: Dict[str, Any]) -> GeneralIncidenceReport:
        """
        Create a GeneralIncidenceReport instance from parsed dictionary data.

        Args:
            parsed_data: Dictionary containing structured emergency data

        Returns:
            GeneralIncidenceReport instance with all relevant information
        """
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
                location=location,
                date=date,
                injured_people=int(medical_data.get('Number of Injured People', 0)),
                severity='medium',  # Default value, should be computed based on injuries
                dest_hospital='TBD',  # To be determined by medical crew
                dist_to_hospital=0.0  # To be calculated based on route
            )

        # Process Fire Report
        fire_report = None
        if fire_data := parsed_data.get('Fire Crew'):
            fire_report = IncidenceFireReport(
                emergency_id=incident_id,
                location=location,
                date=date,
                fire_type=fire_data.get('Fire Nature', 'unknown'),
                severity=fire_data.get('Fire Level (1-5)', 'unknown'),
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
                location=location,
                date=date,
                affected_streets=[],  # To be determined by police crew
                traffic_status=police_data.get('Traffic Status', 'unknown'),
                crowd_size=int(police_data.get('Crowd Size', 0))
            )

        return GeneralIncidenceReport(
            medical=medical_report,
            fire=fire_report,
            police=police_report
        )
