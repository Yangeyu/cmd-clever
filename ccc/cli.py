"""Command-line interface for CCC"""

import argparse
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from . import __version__
from .config import Config
from .agent import CCCAgent

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="CCC (Clever Command-line Companion) - AI-powered terminal assistant"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"CCC version {__version__}"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--model",
        help="AI model to use (default: gpt-4)",
        default=None
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key",
        default=None
    )
    parser.add_argument(
        "--api-base",
        help="Custom API base URL",
        default=None
    )
    parser.add_argument(
        "-n", "--no-stream",
        action="store_true",
        help="Disable streaming mode"
    )
    return parser

def run_interactive_session(agent: CCCAgent, stream: bool = True):
    """Run an interactive session with the agent"""
    history = InMemoryHistory()
    session = PromptSession(history=history)
    
    print(f"CCC v{__version__} - Type 'exit' to quit")
    print("Type your query and press Enter.")
    
    while True:
        try:
            query = session.prompt('> ')

            if query.lower() in ("exit", "quit", "退出"):
                print("Goodbye!")
                break

            agent.process_query(query, stream=stream)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point for CCC"""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        config = Config.from_args(args)
        agent = CCCAgent(config)
        run_interactive_session(agent, stream=not args.no_stream)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            raise
        sys.exit(1)

if __name__ == "__main__":
    main() 