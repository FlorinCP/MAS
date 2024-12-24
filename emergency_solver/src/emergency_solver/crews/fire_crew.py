from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from emergency_solver.schemas.schemas import FirefightingPlan


# Uncomment the following line to use an example of a custom tool
# from emergency_solver.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class FireCrew():
	"""Fire crew"""

	agents_config = 'config/fire_agents.yaml'
	tasks_config = 'config/fire_tasks.yaml'

	@agent
	def commander(self) -> Agent:
		return Agent(
			config=self.agents_config['commander'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def firefighter(self) -> Agent:
		return Agent(
			config=self.agents_config['firefighter'],
			verbose=True
		)

	@agent
	def rescuer(self) -> Agent:
		return Agent(
			config=self.agents_config['rescuer'],
			verbose=True
		)

	@task
	def handle_fire_people_report(self) -> Task:
		return Task(
			config=self.tasks_config['handle_fire_people_report'],
		)

	@task
	def craft_fire_people_action_plan(self) -> Task:
		return Task(
			config=self.tasks_config['craft_fire_people_action_plan'],
			output_pydantic=FirefightingPlan
		)

	@task
	def allocate_fire_extinguishing_resources(self) -> Task:
		return Task(
			config=self.tasks_config['allocate_fire_extinguishing_resources'],
		)

	@task
	def allocate_rescuing_resources(self) -> Task:
		return Task(
			config=self.tasks_config['allocate_rescuing_resources'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the FireCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			verbose=True,
		)
