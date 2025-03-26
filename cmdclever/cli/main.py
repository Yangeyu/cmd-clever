#!/usr/bin/env python
import argparse
import sys
import os
from agno.utils.pprint import pprint_run_response
from cmdclever.agent import CmdAgent
from cmdclever import __version__


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Command-line tool for generating terminal commands",
        prog="cmd-clever",
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "--api-key", 
        help="API key for the Agno API (overrides AGNO_API_KEY environment variable)",
        default=None
    )
    
    parser.add_argument(
        "--api-base", 
        help="Base URL for the Agno API (overrides AGNO_API_BASE environment variable)",
        default=None
    )
    
    parser.add_argument(
        "--model-id", 
        help="Model ID to use (defaults to qwen-plus)",
        default="qwen-plus"
    )
    
    parser.add_argument(
        "--no-stream", 
        help="Disable streaming responses",
        action="store_true",
        default=False
    )
    
    parser.add_argument(
        "--no-execute", 
        help="Disable command execution",
        action="store_true",
        default=False
    )
    
    parser.add_argument(
        "--verbose", 
        help="Enable verbose mode for debugging",
        action="store_true",
        default=False
    )
    
    parser.add_argument(
        "--save", 
        help="Save conversation history to a file when exiting",
        metavar="FILEPATH",
        default=None
    )
    
    parser.add_argument(
        "--load", 
        help="Load conversation history from a file",
        metavar="FILEPATH",
        default=None
    )
    
    parser.add_argument(
        "query", 
        nargs="*", 
        help="Query to send to the command agent"
    )
    
    args = parser.parse_args()
    
    # Create the agent
    try:
        agent = CmdAgent(
            api_key=args.api_key,
            api_base=args.api_base,
            model_id=args.model_id,
            verbose=args.verbose
        )
        
        # Load conversation history if specified
        if args.load:
            if os.path.exists(args.load):
                success = agent.load_conversation(args.load)
                if success:
                    print(f"Loaded conversation history from {args.load}")
                else:
                    print(f"Failed to load conversation history from {args.load}")
            else:
                print(f"Conversation history file not found: {args.load}")
        
    except Exception as e:
        print(f"Error initializing agent: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Print welcome message for interactive mode
    def print_welcome():
        print("\n" + "=" * 60)
        print("       CMD-CLEVER - AI-Powered Command Line Assistant")
        print("=" * 60)
        print("• Type your questions in Chinese or English")
        print("• Commands will be formatted with ```execute``` blocks")
        print("• Commands with ```execute #feedback``` will send output back to AI")
        print("• You'll be asked to confirm before any command is executed")
        print("• Type 'exit', 'quit', or '退出' to exit")
        print("• Working directory:", os.getcwd())
        if args.verbose:
            print("• Verbose mode: ENABLED")
        if args.save:
            print(f"• Conversation will be saved to: {args.save}")
        print("=" * 60 + "\n")
    
    # If no query provided, enter interactive mode
    if not args.query:
        print_welcome()
        
        try:
            while True:
                try:
                    query = input("\n> ")
                    if query.lower() in ("exit", "quit", "退出"):
                        print("Goodbye!")
                        break
                    
                    if not query.strip():
                        continue
                    
                    # Run the agent with the query
                    agent.run(
                        query, 
                        stream=not args.no_stream, 
                        execute=not args.no_execute
                    )
                    
                    # No need to print response here as it's already printed in the agent.run method
                    # This keeps the entire interaction flow in the agent
                    
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"Error: {e}")
            
            # Save conversation history if specified
            if args.save:
                success = agent.save_conversation(args.save)
                if success:
                    print(f"Saved conversation history to {args.save}")
                else:
                    print(f"Failed to save conversation history to {args.save}")
                    
        except KeyboardInterrupt:
            print("\nExiting...")
            # Save on Ctrl+C too
            if args.save:
                success = agent.save_conversation(args.save)
                if success:
                    print(f"Saved conversation history to {args.save}")
                else:
                    print(f"Failed to save conversation history to {args.save}")
    else:
        # Process the command-line query
        query = " ".join(args.query)
        try:
            # Run the agent with the query
            agent.run(
                query, 
                stream=not args.no_stream, 
                execute=not args.no_execute
            )
            
            # Save conversation if needed
            if args.save:
                success = agent.save_conversation(args.save)
                if success:
                    print(f"Saved conversation history to {args.save}")
                else:
                    print(f"Failed to save conversation history to {args.save}")
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main() 