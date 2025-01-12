#!/usr/bin/env python

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start, router

from emergency_solver.src.emergency_solver.crews.combiner_crew import CombinerCrew
from emergency_solver.src.emergency_solver.crews.emergency_crew import EmergencyCrew
from emergency_solver.src.emergency_solver.crews.fire_crew import FireCrew
from emergency_solver.src.emergency_solver.crews.medical_crew import MedicalCrew
from emergency_solver.src.emergency_solver.crews.police_crew import PoliceCrew

def write_output(output, filename):
    with open(filename, "w") as f:
        f.write(output)

class EmergencyState(BaseModel):
    incidence_reports: str = ""
    plans: dict[str, BaseModel] = {}

class EmergencyFlow(Flow[EmergencyState]):

    @start()
    def handle_emergency(self):
        print("Handling emergency report and generating incidence reports for each crew")
        emergency_crew = EmergencyCrew()
        result = emergency_crew.crew().kickoff(inputs={"emergency_report": "./emergency_report.json"})
        self.state.incidence_reports = result.raw
        write_output(self.state.incidence_reports, "emergency_crew_output.json")

    @router(handle_emergency)
    def distribute(self):
        print("Distributing tasks to crews")

        # Kick off the Medical crew if applicable
        if "medical" in self.state.incidence_reports:
            self.state.plans["medical"] = (
                MedicalCrew()
                .crew()
                .kickoff(inputs={
                    "hospitals": "resources/hospitals.json",
                    "ambulances": "resources/ambulances.json",
                    "medical_personnel": "resources/medical_personnel.json"
                })
            )
            write_output(self.state.plans["medical"].raw, "medical_crew_output.txt")

        # Kick off the Police crew if applicable
        if "police" in self.state.incidence_reports:
            self.state.plans["police"] = (
                PoliceCrew()
                .crew()
                .kickoff(inputs={
                    "police_resources": "resources/police_stations.json",
                })
            )
            write_output(self.state.plans["police"].raw, "police_crew_output.md")

        # Kick off the Fire crew if applicable
        if "fire" in self.state.incidence_reports:
            self.state.plans["fire"] = (
                FireCrew()
                .crew()
                .kickoff(inputs={
                    "fire_resources": "resources/fire_stations.json",
                    "rescue_resources": "resources/rescuers.json"
                })
            )
            write_output(self.state.plans["fire"].raw, "fire_crew_output.md")

    @listen(distribute)
    def action_plan(self):
        print("Crafting final Action Plan")
        combiner_crew = CombinerCrew()
        result =  combiner_crew.crew().kickoff({"plans": self.state.plans})
        write_output(result.raw, "final_plan.json")


def kickoff():
    emergency_flow = EmergencyFlow()
    emergency_flow.kickoff()


def plot():
    emergency_flow = EmergencyFlow()
    emergency_flow.plot()


if __name__ == "__main__":
    kickoff()
    #plot()
