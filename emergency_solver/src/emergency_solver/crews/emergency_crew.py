from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, output_pydantic
import litellm

from emergency_solver.schemas.schemas import *


# Uncomment the following line to use an example of a custom tool
# from emergency_solver.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

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
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@task
	def handle_emergency_report(self) -> Task:
		return Task(
			config=self.tasks_config['handle_emergency_report'],
			output_pydantic= GeneralIncidenceReport
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
