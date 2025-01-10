from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from emergency_solver.src.emergency_solver.schemas.schemas import GeneralIncidenceReport, FinalPlan
from emergency_solver.src.emergency_solver.tools.custom_tool import ReadEmergencyReport


llm = LLM(
	model='ollama/llama3.1'
)


@CrewBase
class CombinerCrew():
	"""Emergency crew"""

	agents_config = 'config/combiner_agents.yaml'
	tasks_config = 'config/combiner_tasks.yaml'

	@agent
	def combiner(self) -> Agent:
		return Agent(
			config=self.agents_config['combiner'],
			llm=llm,
			verbose=True
		)


	@task
	def craft_action_plan(self) -> Task:
		return Task(
			config=self.tasks_config['craft_action_plan'],
			output_pydantic=FinalPlan,
			human_input=True
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