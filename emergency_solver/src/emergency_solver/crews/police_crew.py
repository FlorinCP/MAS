from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from emergency_solver.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class PoliceCrew():
	"""Police crew"""

	agents_config = 'config/police_agents.yaml'
	tasks_config = 'config/police_tasks.yaml'

	@agent
	def police(self) -> Agent:
		return Agent(
			config=self.agents_config['police'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def allocator(self) -> Agent:
		return Agent(
			config=self.agents_config['allocator'],
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
