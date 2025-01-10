from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from emergency_solver.src.emergency_solver.schemas.schemas import MedicalPlan
from emergency_solver.src.emergency_solver.tools.custom_tool import ReadResources, RouteDistanceTool

# Uncomment the following line to use an example of a custom tool
# from emergency_solver.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

llm = LLM(
	model='ollama/llama3.1'
)

@CrewBase
class MedicalCrew():
	"""Medical crew"""

	agents_config = 'config/medical_agents.yaml'
	tasks_config = 'config/medical_tasks.yaml'

	@agent
	def doctor(self) -> Agent:
		return Agent(
			config=self.agents_config['doctor'],
			llm=llm,
			verbose=True
		)

	@agent
	def ambulance_technician(self) -> Agent:
		return Agent(
			config=self.agents_config['ambulance_technician'],
			llm=llm,
			tools=[ReadResources(), RouteDistanceTool("zaragoza_graph.graphml")],
			verbose=True
		)

	@task
	def handle_medical_report(self) -> Task:
		return Task(
			config=self.tasks_config['handle_medical_report'],
		)

	@task
	def craft_medical_action_plan(self) -> Task:
		return Task(
			config=self.tasks_config['craft_medical_action_plan'],
			output_pydantic=MedicalPlan
		)

	@task
	def allocate_medical_resources(self) -> Task:
		return Task(
			config=self.tasks_config['allocate_medical_resources'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MedicalCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
