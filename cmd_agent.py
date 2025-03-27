from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import PromptSession
import json
from typing import Optional, Iterator
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow import Workflow, RunResponse, RunEvent
from agno.storage.workflow.sqlite import SqliteWorkflowStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.pprint import pprint_run_response
from agno.utils.log import logger
from agno.models.openai.like import OpenAILike
from textwrap import dedent
from agno.tools.shell import ShellTools
import os


def get_model():
    return OpenAILike(
        id=os.getenv("AI_MODEL") or "gpt-4o",
        base_url=os.getenv("AI_API_BASE") or "https://api.openai.com/v1",
        api_key=os.getenv("AI_API_KEY"),
    )


agent = Agent(
    tools=[ShellTools(), DuckDuckGoTools()],
    instructions=[
        "You are a expert terminal assistant.",
        "First try to use search tool to find the answer.",
    ],
    show_tool_calls=True,
    markdown=True,
    model=get_model(),
    stream=True,
    add_history_to_messages=True,
    num_history_responses=5,
    debug_mode=False,
)

history = InMemoryHistory()
session = PromptSession(history=history)

while True:
    try:
        query = session.prompt('> ')

        if query.lower() in ("exit", "quit", "退出"):
            print("Goodbye!")
            break

        if not query.strip():
            continue

        agent.print_response(query, stream=True)

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"Error: {e}")
