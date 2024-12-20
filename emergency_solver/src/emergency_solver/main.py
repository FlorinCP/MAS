#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start, router

from emergency_solver.src.emergency_solver.crews.emergency_crew import EmergencyCrew
from emergency_solver.src.emergency_solver.crews.fire_crew import FireCrew
from emergency_solver.src.emergency_solver.crews.medical_crew import MedicalCrew
from emergency_solver.src.emergency_solver.crews.police_crew import PoliceCrew


class EmergencyState(BaseModel):
    incidence_reports: dict[str, BaseModel]
    plans: dict[str, BaseModel]


class EmergencyFlow(Flow[EmergencyState]):

    @start()
    def handle_emergency(self):
        print("Handling emergency report and generating incidence reports for each crew")
        result = (EmergencyCrew.crew().kickoff())
        self.state.incidence_reports = result

    @router(handle_emergency)
    def distribute(self):
        print("Distributing tasks to crews")
        if self.state.incidence_reports.medical is not None:
            result = (
                MedicalCrew()
                .crew()
                .kickoff(inputs={"sentence_count": self.state.sentence_count})
            )
        elif self.state.incidence_reports.police is not None:
            result = (
                PoliceCrew()
                .crew()
                .kickoff(inputs={"sentence_count": self.state.sentence_count})
            )
        elif self.state.incidence_reports.fire is not None:
            result = (
                FireCrew()
                .crew()
                .kickoff(inputs={"sentence_count": self.state.sentence_count})
            )

        self.state.plans = result.raw

    @listen(distribute)
    def action_plan(self):
        print("Crafting final Action Plan")
        with open("final_plan.md", "w") as f:
            f.write(self.state.plan)


def kickoff():
    emergency_flow = EmergencyFlow()
    emergency_flow.kickoff()


def plot():
    emergency_flow = EmergencyFlow()
    emergency_flow.plot()


if __name__ == "__main__":
    kickoff()
