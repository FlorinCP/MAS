#!/usr/bin/env python

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start, router

from src.emergency_solver.crews.combiner_crew import CombinerCrew
from src.emergency_solver.crews.emergency_crew import EmergencyCrew
from src.emergency_solver.crews.fire_crew import FireCrew
from src.emergency_solver.crews.medical_crew import MedicalCrew
from src.emergency_solver.crews.police_crew import PoliceCrew
from src.emergency_solver.schemas.schemas import GeneralIncidenceReport


class EmergencyState(BaseModel):
    incidence_reports: GeneralIncidenceReport = None
    plans: dict[str, BaseModel] = {}

class EmergencyFlow(Flow[EmergencyState]):

    @start()
    def handle_emergency(self):
        print("Handling emergency report and generating incidence reports for each crew")
        emergency_crew = EmergencyCrew()
        result = emergency_crew.crew().kickoff(inputs={"emergency_report": "./emergency_report.md"})
        self.state.incidence_reports = result.pydantic
        print(self.state.incidence_reports)

    @router(handle_emergency)
    def distribute(self):
        print("Distributing tasks to crews")
        if self.state.incidence_reports.medical is not None:
            self.state.plans["medical"] = (
                MedicalCrew()
                .crew()
                .kickoff(inputs={"hospitals": "hospitals.json", "ambulances": "ambulances.json", "medical_personnel": "medical_personnel.json"})
            )
        elif self.state.incidence_reports.police is not None:
            self.state.plans["police"] = (
                PoliceCrew()
                .crew()
                .kickoff(inputs={"police_resources": "police_stations.json", })
            )
        elif self.state.incidence_reports.fire is not None:
            self.state.plans["fire"] = (
                FireCrew()
                .crew()
                .kickoff(inputs={"fire_resources": "fire_stations.json", "rescue_resources": "rescue.json"})
            )


    @listen(distribute)
    def action_plan(self):
        print("Crafting final Action Plan")
        combiner_crew = CombinerCrew()
        result =  combiner_crew.crew().kickoff({"plans": self.state.plans})
        with open("final_plan.md", "w") as f:
            f.write(result.raw)


def kickoff():
    emergency_flow = EmergencyFlow()
    emergency_flow.kickoff()


def plot():
    emergency_flow = EmergencyFlow()
    emergency_flow.plot()


if __name__ == "__main__":
    kickoff()
