from crewai import Agent, Crew, Process, Task
from crewai.project import crew, agent, task, CrewBase
from pydantic import BaseModel, Field
from typing import List
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool

class TrendingCompany(BaseModel):
    name: str = Field(description = 'Company Name')
    ticker: str = Field(descripton = 'Stock Ticker Symbol')
    reason: str = Field(description = 'Reason of trending')

class TrendingCompanyList(BaseModel):
    companies: List[TrendingCompany] = Field(description = 'Lsit of trending companies')

class TrendingCompanyResearch(BaseModel):
    name: str = Field(description = 'Company Name')
    market_position: str = Field(description = 'Current Market Position of the company')
    future_outcome: str = Field(description = 'Future outlook and growth Potential')
    investment_potential: str = Field(description = 'Investment Potential')

class TrendingCompanyResearchList(BaseModel):
    research_list: List[TrendingCompanyResearch] = Field(description = 'Comprehensive research on all trending companies')

@CrewBase
class StockPicker():
    """ StockPicker Crew """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config = self.agents_config['trending_company_finder'],
            tools = [SerperDevTool()]
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['financial_researcher'],
            tools = [SerperDevTool()]
        )
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config = self.agents_config['stock_picker'],
            tools = [PushNotificationTool()]
        )
    
    @task 
    def find_trending_companies(self) -> Task:
        return Task(
            config = self.tasks_config['find_trending_companies'],
            output_pydantic = TrendingCompanyList,
        )
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config = self.tasks_config['research_trending_companies'],
            output_pydantic = TrendingCompanyResearchList,
        )
    
    @task
    def pick_best_company(self) -> Task:
        return Task(
            config = self.tasks_config['pick_best_company'],
        )
    
    @crew
    def crew(self) -> Crew:
        manager = Agent(
            config = self.agents_config['manager'],
            allow_delegation = True
        )
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.hierarchical,
            verbose = True,
            manager_agent = manager,
        )