from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Optional


class IncidenceMedicalReport(BaseModel):
    """Output for the Handle emergency report task."""
    emergency_id: int = Field(..., description='Unique identifier for the emergency.')
    location: str = Field(..., description='Address of the emergency.')
    date: datetime = Field(..., description='Date with time of the incident.')
    injured_people: int = Field(..., description='Number of injured people.')
    severity: str = Field(..., description='Severity level of injuries (low, medium, high).')
    dest_hospital: str = Field(..., description='Assigned hospital for transporting patients.')
    dist_to_hospital: float = Field(..., description='Distance to the assigned hospital in kilometers.')

    @classmethod
    def get_schema(cls) -> str:
        schema = '\n'
        for field_name, field_instance in cls.__fields__.items():
            schema += f'{field_name}, described as: {field_instance.description}\n'
        return schema


class IncidenceFireReport(BaseModel):
    """Output for the Handle emergency report task."""
    emergency_id: int = Field(..., description='Unique identifier for the emergency.')
    location: str = Field(..., description='Address of the emergency.')
    date: datetime = Field(..., description='Date with time of the incident.')
    fire_type: str = Field(..., description='Type of fire (ordinary, electrical, gas, chemical).')
    severity: str = Field(..., description='Severity level of fire (low, medium, high).')
    wind_direction: str = Field(..., description='Wind direction (in the compass).')
    wind_speed: str = Field(..., description='Wind speed (in kilometers/hour).')
    affected_area: str = Field(..., description='Total area affected by the fire in square meters.')
    people_to_rescue: int = Field(..., description='Number of people that need to be rescued.')
    required_equipment: List[str] = Field(..., description='Equipment needed to extinguish the fire.')

    @classmethod
    def get_schema(cls) -> str:
        schema = '\n'
        for field_name, field_instance in cls.__fields__.items():
            schema += f'{field_name}, described as: {field_instance.description}\n'
        return schema


class IncidencePoliceReport(BaseModel):
    """Output for the Handle emergency report task."""
    emergency_id: int = Field(..., description='Unique identifier for the emergency.')
    location: str = Field(..., description='Address of the emergency.')
    date: datetime = Field(..., description='Date with time of the incident.')
    affected_streets: List[str] = Field(...,
                                        description='List of streets impacted by the emergency that may require closure.')
    traffic_status: str = Field(...,
                                description='Description of the current traffic conditions (heavy, moderate, clear).')
    crowd_size: int = Field(..., description='Estimated number of people in the affected area.')

    @classmethod
    def get_schema(cls) -> str:
        schema = '\n'
        for field_name, field_instance in cls.__fields__.items():
            schema += f'{field_name}, described as: {field_instance.description}\n'
        return schema

class GeneralIncidenceReport(BaseModel):
    """Combined output for the Handle emergency report task."""
    medical: Optional[IncidenceMedicalReport] = Field(None, description='Medical incidence report.')
    fire: Optional[IncidenceFireReport] = Field(None, description='Fire incidence report.')
    police: Optional[IncidencePoliceReport] = Field(None, description='Police incidence report.')

    @classmethod
    def get_schema(cls) -> str:
        schema = '\n'
        for field_name, field_instance in cls.__fields__.items():
            schema += f'{field_name}, described as: {field_instance.description}\n'
        return schema

class MedicalPlan(BaseModel):
    """Output for the Craft medical crew action plan task."""
    emergency_id: int = Field(..., description='Unique identifier for the emergency.')
    num_ambulances: int = Field(..., description='Total number of ambulances required.')
    ambulance_origins: List[str] = Field(...,
                                         description='List of ambulance stations from where the ambulances will be dispatched.')
    dest_hospital: str = Field(..., description='Name of the hospital where injured people will be attended.')
    required_beds: int = Field(..., description='Number of beds required.')
    personnel: List[str] = Field(..., description='List of required personnel.')

    @classmethod
    def get_schema(cls) -> str:
        schema = '\n'
        for field_name, field_instance in cls.__fields__.items():
            schema += f'{field_name}, described as: {field_instance.description}\n'
        return schema


class FirefightingPlan(BaseModel):
    """Output for the Craft fire people action plan task."""
    emergency_id: int = Field(..., description='Unique identifier for the emergency.')
    num_firetrucks: int = Field(..., description='Total number of fire trucks.')
    types_firetrucks: List[str] = Field(...,
                                        description='Type of fire trucks (fire-extinguisher, with ladder, without...).')
    fire_stations_involved: List[str] = Field(...,
                                              description='List of fire stations contributed resources to the operation.')
    rescue_equipment: List[str] = Field(..., description='List of equipment required for rescuing.')
    personnel: List[str] = Field(..., description='List of required personnel.')

    @classmethod
    def get_schema(cls) -> str:
        schema = '\n'
        for field_name, field_instance in cls.__fields__.items():
            schema += f'{field_name}, described as: {field_instance.description}\n'
        return schema


class PolicePlan(BaseModel):
    """Output for the Craft police crew action plan task."""
    emergency_id: int = Field(..., description='Unique identifier for the emergency.')
    num_patrols: int = Field(..., description='Total number of police patrols.')
    patrol_stations_involved: List[str] = Field(...,
                                                description='Names of police stations sending patrols to the emergency.')
    traffic_redir: List[str] = Field(..., description='Suggested alternative routes for redirecting traffic.')
    evacuation_plan: str = Field(..., description='Details of the evacuation strategy.')

    @classmethod
    def get_schema(cls) -> str:
        schema = '\n'
        for field_name, field_instance in cls.__fields__.items():
            schema += f'{field_name}, described as: {field_instance.description}\n'
        return schema


class FinalPlan(BaseModel):
    """Output for the Craft action plan task."""
    emergency_id: int = Field(..., description='Unique identifier for the emergency.')
    date: datetime = Field(..., description='Date with time of the incident.')
    police_plan: PolicePlan = Field(..., description='Police strategy for the final plan.')
    firefighting_plan: FirefightingPlan = Field(..., description='Firefighting strategy for the final plan.')
    medical_plan: FirefightingPlan | None = Field(..., description='Medical strategy for the final plan.')

    @classmethod
    def get_schema(cls) -> str:
        schema = '\n'
        for field_name, field_instance in cls.__fields__.items():
            schema += f'{field_name}, described as: {field_instance.description}\n'
        return schema
