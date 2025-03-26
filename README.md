# Cmd Clever

A command-line tool for generating and executing terminal commands using AI.

## Installation

```bash
pip install cmd-clever
```

## Usage

### Command-line Arguments

```bash
# Basic usage with a query
cmd-clever 查找大于100MB的日志文件

# Specify API key and base URL
cmd-clever --api-key your-api-key --api-base your-api-base 查找最近修改的文件

# Use a different model ID
cmd-clever --model-id different-model-id 创建一个新的目录并将文件移动到其中

# Disable streaming output
cmd-clever --no-stream 查找包含特定文本的文件

# Disable command execution
cmd-clever --no-execute 查找包含特定文本的文件

# Enable verbose mode for debugging
cmd-clever --verbose 分析系统性能

# Save conversation history to a file
cmd-clever --save conversation.json 查找大文件

# Load previous conversation history
cmd-clever --load conversation.json

# Combine multiple options
cmd-clever --verbose --save debug_session.json --model-id gpt-4 分析磁盘使用情况
```

### Interactive Mode

If you don't provide a query, Cmd Clever enters interactive mode:

```bash
cmd-clever
```

You can then input your queries one by one and get responses. Type "exit" or "quit" to leave interactive mode.

### Command Execution

Cmd Clever can execute commands for you:

1. When you ask a question, Cmd Clever will generate commands in a special format:
   ```execute
   <command>
   ```

2. You'll be asked to confirm before any command is executed
3. Execution results will be displayed and saved in the conversation history
4. History is only kept for the current session

Example workflow:
```
> 查找当前目录下所有的 Python 文件

I'll help you find all Python files in the current directory.

```execute
find . -name "*.py" -type f
```

----------------------------------------
Command to execute:
find . -name "*.py" -type f
----------------------------------------
Execute this command? (y/n): y

Executing command...

----------------------------------------
Command output:
----------------------------------------
./setup.py
./cmdclever/__init__.py
./cmdclever/__main__.py
./cmdclever/cli/__init__.py
./cmdclever/cli/main.py
./cmdclever/agent.py
```

### Command Feedback Loop

Cmd Clever supports a feedback loop for commands that need further analysis:

1. Commands marked with `#feedback` will send their output back to the AI for analysis:
   ```execute #feedback
   <command>
   ```

2. After executing such a command, the output is sent to the AI model
3. The model analyzes the output and can suggest new commands
4. These new commands are added to the execution queue

Example workflow:
```
> 分析当前系统的磁盘使用情况

让我检查您的磁盘使用情况，首先查看磁盘分区情况：

```execute #feedback
df -h
```

----------------------------------------
Command to execute (with feedback):
df -h
----------------------------------------
Execute this command? (y/n): y

Executing command...

----------------------------------------
Command output:
----------------------------------------
Filesystem      Size   Used  Avail Capacity   iused    ifree %iused  Mounted on
/dev/disk1s2   466Gi   11Gi  289Gi     4%    486175 2861779825    0%   /
/dev/disk1s1   466Gi  147Gi  289Gi    34%   1911713 2860354287    0%   /System/Volumes/Data

Sending command output back to model for analysis...

----------------------------------------
Model's response to command output:
----------------------------------------
我看到您的系统有充足的磁盘空间。主分区使用了34%，系统分区仅使用了4%。

让我们看看哪些目录占用了最多空间：

```execute
du -h -d 1 ~ | sort -hr | head -n 5
```

这个命令会显示您的主目录下占用空间最多的5个目录。

Added 1 new command(s) based on feedback analysis.
```

### Verbose Mode

Verbose mode provides detailed information about what's happening during command execution, which is helpful for debugging or understanding the internal workflow:

```bash
cmd-clever --verbose
```

In verbose mode, you'll see additional information:
- API connections and model usage
- Command extraction details
- Command execution steps
- Response processing information
- Feedback loop analysis

Example verbose output:
```
[VERBOSE] Initialized CmdAgent with model: qwen-plus
[VERBOSE] Using API base: https://api.example.com
[VERBOSE] Conversation history initialized
[VERBOSE] Created OpenAILike model with ID: qwen-plus
...
[VERBOSE] Extracted 2 commands from response
[VERBOSE] Command 1: find /home -type f -name "*.log" -size... (feedback: True)
[VERBOSE] Command execution is enabled
...
```

### Saving and Loading Conversations

You can save and load conversation history:

```bash
# Save the conversation to a file
cmd-clever --save conversation.json

# Load a previous conversation
cmd-clever --load conversation.json
```

This is useful for:
- Continuing a previous session
- Reviewing past command executions
- Sharing conversation history with others
- Debugging issues

### Environment Variables

Cmd Clever looks for the following environment variables:

- `AGNO_API_KEY`: Your API key
- `AGNO_API_BASE`: Your API base URL

You can set these in your shell configuration (e.g., `.bashrc`, `.zshrc`) to avoid specifying them on each run:

```bash
export AGNO_API_KEY="your-api-key"
export AGNO_API_BASE="your-api-base"
```

## Features

- Accepts queries in Chinese and English
- Generates safe and reliable terminal commands
- Automatically executes commands with user confirmation
- Records command execution results in the conversation
- Supports feedback loops for command output analysis
- Automatically adapts commands for Linux/macOS
- Warns about potentially dangerous operations
- Supports command explanations
- Interactive and one-off query modes
- Verbose mode for debugging
- Save and load conversation history

## License

MIT 