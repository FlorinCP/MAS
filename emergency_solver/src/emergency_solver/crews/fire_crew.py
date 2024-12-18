from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

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

	@crew
	def crew(self) -> Crew:
		"""Creates the EmergencySolver crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
