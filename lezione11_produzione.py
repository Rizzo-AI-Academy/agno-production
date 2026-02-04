from agno.team import Team
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
# load_dotenv()
import os
from agno.agent import Agent
from agno.os import AgentOS
from fastapi.middleware.cors import CORSMiddleware

news_agent = Agent(
    id="news_agent",
    name="News Agent",
    role="Get trending tech news from HackerNews",
    tools=[HackerNewsTools()]
)

finance_agent = Agent(
    id="finance_agent",
    name="Finance Agent",
    role="Get stock prices and financial data",
    tools=[YFinanceTools()]
)
# read api key from env
api_key = os.getenv("OPENAI_API_KEY")

team = Team(
    id="team1",
    name="Research Team",
    members=[news_agent, finance_agent],
    model=OpenAIResponses(id="gpt-4.1", api_key=api_key),
    instructions="Delegate to the appropriate agent based on the request.",
)

agent_os = AgentOS(teams=[team], agents=[news_agent, finance_agent])
app = agent_os.get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)