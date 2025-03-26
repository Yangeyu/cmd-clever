import os
import re
import subprocess
import json
from textwrap import dedent
from typing import Optional, Dict, Any, List, Tuple

from agno.agent import Agent
from agno.utils.pprint import pprint_run_response
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.openai.like import OpenAILike


class CmdAgent:
    """Terminal Command Assistant agent."""
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None, 
                model_id: str = "qwen-plus", verbose: bool = False):
        """Initialize the command agent with API configuration.
        
        Args:
            api_key: The API key to use. If None, uses the AGNO_API_KEY environment variable.
            api_base: The API base URL. If None, uses the AGNO_API_BASE environment variable.
            model_id: The model ID to use, defaults to "qwen-plus".
            verbose: Whether to enable verbose output for debugging.
        """
        self.api_key = api_key or os.getenv("AGNO_API_KEY")
        self.api_base = api_base or os.getenv("AGNO_API_BASE")
        self.model_id = model_id
        self.verbose = verbose
        
        if not self.api_key:
            raise ValueError("API key must be provided either through AGNO_API_KEY environment variable or --api-key parameter")
        
        if not self.api_base:
            raise ValueError("API base URL must be provided either through AGNO_API_BASE environment variable or --api-base parameter")
        
        self.instructions = self._get_instructions()
        self.agent = self._create_agent()
        self.conversation_history = []
        
        if self.verbose:
            print(f"\n[VERBOSE] Initialized CmdAgent with model: {self.model_id}")
            print(f"[VERBOSE] Using API base: {self.api_base}")
            print(f"[VERBOSE] Conversation history initialized")
    
    def _get_model(self):
        """Get the model for the agent."""
        model = OpenAILike(
            id=self.model_id,
            api_key=self.api_key,
            base_url=self.api_base,
        )
        
        if self.verbose:
            print(f"[VERBOSE] Created OpenAILike model with ID: {self.model_id}")
            
        return model
    
    def _get_instructions(self):
        """Get the instructions for the agent."""
        instructions = dedent(
            """
            # Role: Terminal Command Assistant

            ## Profile
            **Name**: Command Assistant
            **Specialty**: 生成安全可靠的终端命令  
            **Language**: 中文提问，优先返回英文命令  
            **Description**: 专为开发者设计的终端命令生成专家，支持Linux/macOS双平台
            **Limitations**:
                - 根据用户的问题先联网查询，然后生成命令


            ## Skills
            - 精准解析自然语言需求
            - 自动识别潜在危险操作
            - 多平台命令适配
            - 常用命令缓存优化
            - 复杂管道组合
            - 命令执行效果预测

            ## Format Requirements
            1. 当需要执行命令时，使用以下格式包装命令：
               ```execute
               <command>
               ```
            2. 如果需要获取命令输出结果进行进一步分析，使用以下格式：
               ```execute #feedback
               <command>
               ```
            3. 这种格式让用户清楚知道哪些是可执行命令，并且能方便系统解析
            4. 不要在同一个代码块中包含多条不同命令，应分开为多个execute块
            5. 对于危险命令，请添加警告标识
            6. 当使用带 #feedback 标记的命令时，你将能够收到执行结果并进行进一步分析

            ## Workflow
            1. **需求解析**：分析用户query的真实意图
            2. **命令生成**：按优先级输出方案，并使用execute标识：
               ```execute
               <具体命令>
               ```
            3. **安全检查**：扫描命令中的危险模式（rm -rf、权限提升等）
            4. **平台适配**：检测到macOS时自动替换gsed/gawk等brew命令
            5. **解释说明**：使用中文注释关键参数
            6. **结果分析**：当命令带有 #feedback 标记时，你会收到执行结果并可以据此提供进一步的命令或分析

            ## Constraints
            - 如果用户的问题与命令无关，返回'How can I help you?'
            - 当请求包含危险操作时，必须添加❗️emoji警告
            - 优先使用系统内置工具（避免依赖安装）
            - 组合命令不超过3个管道符
            - 不解释基础命令（如ls/cd等）
            - 需要sudo权限时给出明确提示
            - 需要解释指令的作用
            - 输出的内容在50字左右
            - 当你需要先了解环境信息时，使用 #feedback 标记命令

            ## Examples
            **用户输入**：找出/home下所有超过1G的日志文件并显示

            **Response**：
            以下命令可以找出 /home 目录下超过 1G 的日志文件并显示详细信息：

            ```execute #feedback
            find /home -type f -name "*.log" -size +1G -exec ls -lh {} \;
            ```

            这个命令会搜索 /home 目录中所有 .log 文件，筛选出大于 1G 的文件，并使用 ls -lh 显示它们的详细信息和人类可读的大小格式。
            
            **系统反馈命令执行结果**
            
            **Response**：
            根据执行结果，我看到以下大文件：
            
            如果你想删除这些文件，可以使用：
            
            ```execute
            find /home -type f -name "*.log" -size +1G -exec rm {} \;
            ```
            
            请注意，删除前建议先备份重要数据。
            """
        )
        
        if self.verbose:
            print(f"[VERBOSE] Generated system instructions ({len(instructions)} chars)")
            
        return instructions
    
    def _create_agent(self):
        """Create the agent with the given configuration."""
        agent = Agent(
            model=self._get_model(),
            instructions=self.instructions,
            tools=[DuckDuckGoTools()],
            show_tool_calls=True,
            markdown=True,
        )
        
        if self.verbose:
            print(f"[VERBOSE] Created Agent with DuckDuckGoTools")
            
        return agent
    
    def extract_commands(self, text: str) -> List[Tuple[str, bool]]:
        """Extract commands from the agent's response.
        
        Args:
            text: The agent's response text.
            
        Returns:
            List of tuples (command, needs_feedback) where needs_feedback is a boolean.
        """
        # Match content inside ```execute blocks, with optional #feedback tag
        pattern = r"```execute(\s+#feedback)?\s*(.*?)\s*```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        # Clean up commands and determine if feedback is needed
        commands = []
        for feedback_tag, cmd in matches:
            needs_feedback = bool(feedback_tag.strip())
            commands.append((cmd.strip(), needs_feedback))
        
        if self.verbose:
            print(f"[VERBOSE] Extracted {len(commands)} commands from response")
            for i, (cmd, needs_feedback) in enumerate(commands):
                print(f"[VERBOSE] Command {i+1}: {cmd[:40]}... (feedback: {needs_feedback})")
        
        return commands
    
    def execute_command(self, command: str) -> Tuple[bool, str]:
        """Execute a shell command and return the result.
        
        Args:
            command: The command to execute.
            
        Returns:
            Tuple of (success, output) where success is a boolean and output is the command output.
        """
        if self.verbose:
            print(f"[VERBOSE] Executing command: {command}")
            print(f"[VERBOSE] Current working directory: {os.getcwd()}")
        
        try:
            # Use absolute path to project directory
            current_dir = os.getcwd()
            
            if self.verbose:
                print(f"[VERBOSE] Starting subprocess with shell=True")
                
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=current_dir
            )
            
            if self.verbose:
                print(f"[VERBOSE] Command completed with return code: {result.returncode}")
                print(f"[VERBOSE] Stdout size: {len(result.stdout)} chars")
                print(f"[VERBOSE] Stderr size: {len(result.stderr)} chars")
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"[VERBOSE] Command executed successfully")
                return True, result.stdout
            else:
                if self.verbose:
                    print(f"[VERBOSE] Command failed with code {result.returncode}")
                    print(f"[VERBOSE] Error: {result.stderr}")
                return False, f"Error (code {result.returncode}):\n{result.stderr}"
        except Exception as e:
            if self.verbose:
                print(f"[VERBOSE] Exception during command execution: {str(e)}")
            return False, f"Failed to execute command: {str(e)}"
    
    def _get_response(self, query: str, stream: bool = True) -> str:
        """Get response from the agent.
        
        Args:
            query: The query to send to the agent.
            stream: Whether to stream the response.
            
        Returns:
            The response text.
        """
        if self.verbose:
            print(f"[VERBOSE] Sending query to agent (stream={stream}): {query[:50]}...")
        
        try:
            # Get the agent's response
            if stream:
                if self.verbose:
                    print(f"[VERBOSE] Using streaming mode")
                
                # For streaming mode, collect the full response
                full_response = ""
                response_generator = self.agent.run(query, stream=True)
                
                chunk_count = 0
                for chunk in response_generator:
                    chunk_count += 1
                    # Handle different chunk formats
                    if hasattr(chunk, 'content'):
                        # Object with content attribute
                        chunk_text = chunk.content
                        full_response += chunk_text
                    elif isinstance(chunk, str):
                        # String chunk
                        chunk_text = chunk
                        full_response += chunk_text
                    elif isinstance(chunk, dict) and 'content' in chunk:
                        # Dictionary with content key
                        chunk_text = chunk['content']
                        full_response += chunk_text
                    else:
                        # Try string conversion for other types
                        try:
                            chunk_text = str(chunk)
                            full_response += chunk_text
                        except:
                            if self.verbose:
                                print(f"[VERBOSE] Could not convert chunk to string: {type(chunk)}")
                            pass  # Skip if can't convert
                    
                    if self.verbose and chunk_count % 10 == 0:
                        print(f"[VERBOSE] Received {chunk_count} chunks so far, current length: {len(full_response)}")
                            
                response_text = full_response
                
                if self.verbose:
                    print(f"[VERBOSE] Streaming complete, received {chunk_count} chunks")
                    print(f"[VERBOSE] Final response length: {len(response_text)} chars")
            else:
                if self.verbose:
                    print(f"[VERBOSE] Using non-streaming mode")
                
                # For non-streaming mode
                response = self.agent.run(query, stream=False)
                
                if self.verbose:
                    print(f"[VERBOSE] Received response of type: {type(response)}")
                
                if hasattr(response, 'content'):
                    response_text = response.content
                    if self.verbose:
                        print(f"[VERBOSE] Extracted content attribute")
                elif isinstance(response, dict) and 'content' in response:
                    response_text = response['content']
                    if self.verbose:
                        print(f"[VERBOSE] Extracted content from dictionary")
                elif isinstance(response, str):
                    response_text = response
                    if self.verbose:
                        print(f"[VERBOSE] Response was already a string")
                else:
                    response_text = str(response)
                    if self.verbose:
                        print(f"[VERBOSE] Converted response to string")
                
                if self.verbose:
                    print(f"[VERBOSE] Final response length: {len(response_text)} chars")
            
            return response_text
        except Exception as e:
            error_msg = f"Error getting response: {str(e)}"
            if self.verbose:
                print(f"[VERBOSE] Exception during get_response: {str(e)}")
            return error_msg
    
    def run(self, query: str, stream: bool = True, execute: bool = True):
        """Run the agent with the given query.
        
        Args:
            query: The query to ask the agent.
            stream: Whether to stream the response.
            execute: Whether to execute commands.
            
        Returns:
            The agent's response with command execution results if execute=True.
        """
        if self.verbose:
            print(f"\n[VERBOSE] ===== Starting new run =====")
            print(f"[VERBOSE] Query: {query}")
            print(f"[VERBOSE] Parameters: stream={stream}, execute={execute}")
            print(f"[VERBOSE] Current history length: {len(self.conversation_history)}")
        
        # Add query to conversation history
        self.conversation_history.append({"role": "user", "content": query})
        
        if self.verbose:
            print(f"[VERBOSE] Added user query to conversation history")
        
        # Get initial response
        response_text = self._get_response(query, stream=stream)
        
        # Add agent response to history
        self.conversation_history.append({"role": "assistant", "content": response_text})
        
        if self.verbose:
            print(f"[VERBOSE] Added assistant response to conversation history")
            print(f"[VERBOSE] History now has {len(self.conversation_history)} messages")
        
        # Handle command execution if enabled
        if execute:
            if self.verbose:
                print(f"[VERBOSE] Command execution is enabled")
            
            # Extract commands from the response
            commands = self.extract_commands(response_text)
            
            if self.verbose:
                print(f"[VERBOSE] Beginning execution of {len(commands)} commands")
            
            # Process each command
            i = 0
            while i < len(commands):
                cmd, needs_feedback = commands[i]
                
                if self.verbose:
                    print(f"\n[VERBOSE] Processing command {i+1}/{len(commands)}")
                    print(f"[VERBOSE] Command: {cmd}")
                    print(f"[VERBOSE] Needs feedback: {needs_feedback}")
                
                print("\n" + "-" * 40)
                print(f"Command to execute{' (with feedback)' if needs_feedback else ''}:\n{cmd}")
                print("-" * 40)
                
                confirmation = input("Execute this command? (y/n): ").lower()
                
                if confirmation == 'y':
                    if self.verbose:
                        print(f"[VERBOSE] User confirmed execution")
                    
                    print("\nExecuting command...\n")
                    success, output = self.execute_command(cmd)
                    
                    print("\n" + "-" * 40)
                    print("Command output:")
                    print("-" * 40)
                    print(output)
                    
                    # Add execution result to conversation history
                    result_content = f"Command execution {'succeeded' if success else 'failed'}:\n\n```\n{output}\n```"
                    self.conversation_history.append({
                        "role": "system", 
                        "content": result_content
                    })
                    
                    if self.verbose:
                        print(f"[VERBOSE] Added command result to history")
                        print(f"[VERBOSE] History now has {len(self.conversation_history)} messages")
                    
                    # If feedback is needed, send the result back to the model
                    if needs_feedback:
                        if self.verbose:
                            print(f"[VERBOSE] Command requires feedback, sending result to model")
                        
                        print("\nSending command output back to model for analysis...\n")
                        
                        # Create feedback query
                        feedback_query = f"I executed the command and got the following result:\n\n{result_content}\n\nPlease analyze this output and provide further guidance or commands if needed."
                        
                        if self.verbose:
                            print(f"[VERBOSE] Feedback query: {feedback_query[:100]}...")
                        
                        # Get response with feedback
                        feedback_response = self._get_response(feedback_query, stream=stream)
                        
                        # Add feedback response to history
                        self.conversation_history.append({"role": "assistant", "content": feedback_response})
                        
                        if self.verbose:
                            print(f"[VERBOSE] Added feedback response to history")
                            print(f"[VERBOSE] History now has {len(self.conversation_history)} messages")
                        
                        print("\n" + "-" * 40)
                        print("Model's response to command output:")
                        print("-" * 40)
                        print(feedback_response)
                        
                        # Extract new commands from the feedback response
                        new_commands = self.extract_commands(feedback_response)
                        
                        # Add new commands to the queue
                        if new_commands:
                            old_length = len(commands)
                            # Insert new commands after the current one
                            commands = commands[:i+1] + new_commands + commands[i+1:]
                            new_length = len(commands)
                            
                            if self.verbose:
                                print(f"[VERBOSE] Added {len(new_commands)} new commands from feedback")
                                print(f"[VERBOSE] Command queue expanded from {old_length} to {new_length}")
                            
                            print(f"\nAdded {len(new_commands)} new command(s) based on feedback analysis.")
                else:
                    if self.verbose:
                        print(f"[VERBOSE] User skipped command execution")
                    
                    print("Command execution skipped.")
                    self.conversation_history.append({
                        "role": "system", 
                        "content": "Command execution skipped by user."
                    })
                
                # Move to the next command
                i += 1
            
            if self.verbose:
                print(f"\n[VERBOSE] Completed processing all {len(commands)} commands")
        else:
            if self.verbose:
                print(f"[VERBOSE] Command execution is disabled")
        
        if self.verbose:
            print(f"[VERBOSE] Run completed, final history length: {len(self.conversation_history)}")
            print(f"[VERBOSE] ===== Run complete =====\n")
        
        # Return the final response text
        return response_text
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        
        if self.verbose:
            print(f"[VERBOSE] Conversation history cleared")
    
    def save_conversation(self, filepath: str) -> bool:
        """Save the conversation history to a file.
        
        Args:
            filepath: Path to save the conversation history.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.verbose:
                print(f"[VERBOSE] Saving conversation to {filepath}")
                
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
                
            if self.verbose:
                print(f"[VERBOSE] Successfully saved conversation with {len(self.conversation_history)} messages")
                
            return True
        except Exception as e:
            if self.verbose:
                print(f"[VERBOSE] Failed to save conversation: {str(e)}")
            return False
    
    def load_conversation(self, filepath: str) -> bool:
        """Load conversation history from a file.
        
        Args:
            filepath: Path to load the conversation history from.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            if self.verbose:
                print(f"[VERBOSE] Loading conversation from {filepath}")
                
            with open(filepath, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
                
            if self.verbose:
                print(f"[VERBOSE] Successfully loaded conversation with {len(self.conversation_history)} messages")
                
            return True
        except Exception as e:
            if self.verbose:
                print(f"[VERBOSE] Failed to load conversation: {str(e)}")
            return False 