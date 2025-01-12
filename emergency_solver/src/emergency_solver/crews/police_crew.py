from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from emergency_solver.src.emergency_solver.schemas.schemas import PolicePlan
from emergency_solver.src.emergency_solver.tools.custom_tool import ReadResources, RouteDistanceTool

# Uncomment the following line to use an example of a custom tool
# from emergency_solver.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

llm = LLM(
	model='ollama/llama3.1'
)

@CrewBase
class PoliceCrew():
	"""Police crew"""

	agents_config = 'config/police_agents.yaml'
	tasks_config = 'config/police_tasks.yaml'

	@agent
	def police(self) -> Agent:
		return Agent(
			config=self.agents_config['police'],
			llm=llm,
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def allocator(self) -> Agent:
		return Agent(
			config=self.agents_config['allocator'],
			llm=llm,
			tools=[ReadResources(), RouteDistanceTool("zaragoza_graph.graphml")],
			verbose=True
		)

	@task
	def handle_police_report(self) -> Task:
		return Task(
			config=self.tasks_config['handle_police_report'],
		)

	@task
	def block_streets(self) -> Task:
		return Task(
			config=self.tasks_config['block_streets'],
		)

	@task
	def craft_police_action_plan(self) -> Task:
		return Task(
			config=self.tasks_config['craft_police_action_plan'],
		)

	@task
	def allocate_police_resources(self) -> Task:
		return Task(
			config=self.tasks_config['allocate_police_resources'],
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
