import os
from crewai import Agent, Crew, Task, Process
from crewai.crew import EntityMemory
from crewai.project import crew, agent, task, CrewBase
from pydantic import BaseModel, Field
from typing import List, Optional
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

gemini_embedder_config = {
    'provider':'google',
    'config': {
        'model':'embedding-001',
        'api_key': os.environ['GEMINI_API_KEY']
    }
}
class TrendingCompany(BaseModel):
    name: str = Field(description = 'Indian Company Name')
    ticker: str = Field(description = 'NSE/BSE Stock Ticker Symbol (e.g., RELIANCE, TCS, INFY)')
    exchange: str = Field(description = 'Primary exchange - NSE or BSE')
    markert_cap_cr: Optional[str] = Field(description = ' Market capitalization in ₹ crores')
    sector: str = Field(description = 'Indian business sector (IT, Banking Pharma, FMCG, etc.)')
    reason: str = Field(description = 'Specific reason for trending in Indian financial news')
    news_source: str = Field(description = 'Source of trending news (ET, BS, Mint, MoneyControl)')

class TrendingCompanyList(BaseModel):
    companies: List[TrendingCompany] = Field(description = 'List of trending Indian companies')
    analysis_date: str = Field(description = 'Date of analysis')
    market_context: str = Field(description = 'Current Nifty/Sensex trend context')

class TrendingCompanyResearch(BaseModel):
    name: str = Field(description = 'Indian Company Name')
    ticker: str = Field(description = 'NSE/BSE ticker symbol')
    exchange: str = Field(description = 'Primary exchange (NSE/BSE)')
    current_price: Optional[float] = Field(description = 'Current stock price in ₹')
    market_cap_cr: Optional[float] = Field(description = 'Market cap in ₹ crores')
    pe_ratio: Optional[float] = Field(description = 'Price to Earnings ratio')
    promoter_holding: Optional[float] = Field(description = 'Promoter holding precentage')
    market_position: str = Field(description = 'Market position in Indian industry')
    financial_highlights: str = Field(description = 'Key financial metrics in INR')
    competitive_analysis: str = Field(description = 'Competition analysis in Indian market')
    future_outcome: str = Field(description = 'Future oulook considering Indian economic growth')
    investment_potential: str = Field(description = 'Investment potential with Indian market risks')
    sebi_compliance: str = Field(description = 'SEBI compliance and governance status')
    liquidity_analysis: str = Field(description = 'Trading liquidity on NSE/BSE')

class TrendingCompanyResearchList(BaseModel):
    research_list: List[TrendingCompanyResearch] = Field(description = 'Comprehensive research on trending Indian companies')
    market_summary: str = Field(description = 'Overall Indian equity market summary')
    sector_outlook: str = Field(description = 'Sector-wise outlook for Indian market')

class StockPickerDecision(BaseModel):
    selected_company: str = Field(description = 'Selected Indian company name')
    ticker: str = Field(description = 'NSE/BSE ticker symbol')
    exchange: str = Field(description = 'Primary exchange (NSE/BSE)')
    investment_rationale: str = Field(description = 'Detailed investment rationale for Indian market')
    target_price: Optional[str] = Field(description = 'Target price in ₹')
    investment_horizon: str = Field(description = 'Recommended investment time horizon')
    key_strengths: List[str] = Field(description = 'Key strengths in Indian market context')
    risk_factors: List[str] = Field(description = 'Risk factors specific to Indian market')
    rejected_companies: List[dict] = Field(description = 'Other companies analyzed with rejection reasons')

@CrewBase
class StockPicker():
    """ Indian Stock Picker Crew """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config = self.agents_config['trending_company_finder'],
            tools = [SerperDevTool()],
            verbose = True,
            memory = True
        )
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['financial_researcher'],
            tools = [SerperDevTool()],
            verbose = True,
            memory = True
        )
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config = self.agents_config['stock_picker'],
            tools = [PushNotificationTool()],
            verbose = True,
            memory = True
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
            output_pydantic = StockPickerDecision,
        )
    
    @crew
    def crew(self) -> Crew:
        manager = Agent(
            config = self.agents_config['manager'],
            allow_delegation = True,
            verbose = True
        )

        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.hierarchical,
            verbose = True,
            manager_agent = manager,
            memory = True,
            # Long-term memory for persistent storage across sessions
            long_term_memory = LongTermMemory(
                storage = LTMSQLiteStorage(
                    db_path = './memory/long_term_memory_storage.db'
                )
            ),
            # Short-term memory for current context using RAG
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                    embedder_config = gemini_embedder_config,
                    type = 'short_term',
                    path = './memory/'
                )
            ),
            # Entity memory for tracking key information about entities
            entity_memory = EntityMemory(
                storage = RAGStorage(
                    embedder_config = gemini_embedder_config,
                    type = 'short_term',
                    path = './memory/'
                )
            ),
        )