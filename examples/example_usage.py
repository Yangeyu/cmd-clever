#!/usr/bin/env python
"""
Example script showing how to use the CmdAgent programmatically.
"""

import os
from cmdclever.agent import CmdAgent

def main():
    """Run a simple example of using CmdAgent."""
    
    # Get API credentials from environment variables
    api_key = os.getenv("AGNO_API_KEY")
    api_base = os.getenv("AGNO_API_BASE")
    
    if not api_key or not api_base:
        print("Error: Please set AGNO_API_KEY and AGNO_API_BASE environment variables.")
        return
    
    # Create agent
    agent = CmdAgent(api_key=api_key, api_base=api_base)
    
    # Run a query that will involve command feedback
    query = "分析当前目录中文件的类型分布并推荐整理方法"
    print(f"Query: {query}\n")
    
    # Get response and execute commands with feedback enabled
    response_text = agent.run(query, stream=True, execute=True)
    
    # Print the final response if needed
    print("\nFinal Response Text:")
    print("-" * 40)
    print(response_text)
    
    # Print conversation history
    print("\nConversation History:")
    for i, message in enumerate(agent.conversation_history):
        role = message["role"]
        content = message["content"]
        print(f"\n[{i+1}. {role.upper()}]")
        print("-" * 40)
        print(content)
    
    # Clear history if needed
    # agent.clear_history()
    
    print("\n" + "=" * 60)
    print("Example of command execution with feedback loop:")
    print("=" * 60)
    print("1. The initial query asked to analyze file types in current directory")
    print("2. The AI generated a command with #feedback tag")
    print("3. After execution, the output was sent back to the AI")
    print("4. The AI analyzed the results and suggested new commands")
    print("5. These commands were added to the execution queue")
    print("=" * 60)

if __name__ == "__main__":
    main() 