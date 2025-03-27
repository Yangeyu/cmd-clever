"""AI agent functionality for CCC"""

from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.shell import ShellTools
from agno.tools.duckduckgo import DuckDuckGoTools

from .config import Config

class CCCAgent:
    """CCC AI Agent wrapper"""
    
    def __init__(self, config: Config):
        """Initialize the agent with configuration"""
        self.config = config
        self.model = OpenAILike(
            id=config.model,
            base_url=config.api_base,
            api_key=config.api_key,
        )
        
        self.agent = Agent(
            tools=[ShellTools(), DuckDuckGoTools()],
            instructions=[
                "You are an expert terminal assistant.",
                "First try to use search tool to find the answer.",
            ],
            show_tool_calls=True,
            markdown=True,
            model=self.model,
            stream=True,
            add_history_to_messages=True,
            num_history_responses=5,
            debug_mode=config.debug,
        )
    
    def process_query(self, query: str, stream: bool = True) -> None:
        """Process a single query and print the response"""
        if not query.strip():
            return
            
        self.agent.print_response(query, stream=stream) 