from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from emergency_solver.src.emergency_solver.schemas.schemas import GeneralIncidenceReport, FinalPlan
from emergency_solver.src.emergency_solver.tools.custom_tool import ReadEmergencyReport, CraftGeneralIncidenceReport

llm = LLM(
	model='ollama/llama3.1'
)


@CrewBase
class EmergencyCrew():
	"""Emergency crew"""

	agents_config = 'config/emergency_agents.yaml'
	tasks_config = 'config/emergency_tasks.yaml'

	@agent
	def dispatcher(self) -> Agent:
		return Agent(
			config=self.agents_config['dispatcher'],
			llm=llm,
			verbose=True
		)

	@task
	def handle_emergency_report(self) -> Task:
		return Task(
			config=self.tasks_config['handle_emergency_report'],
			tools=[ReadEmergencyReport(), CraftGeneralIncidenceReport(result_as_answer=True)],
			verbose=True
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the EmergencyCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)