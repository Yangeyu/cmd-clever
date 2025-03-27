# CCC (Clever Command-line Companion)

A smart command-line assistant powered by AI that helps you with terminal commands and tasks.

## Installation

```bash
pip install ccc-cli-helper
```

## Usage

Start the assistant:
```bash
ccc
```

Options:
- `-h, --help`: Show help message
- `-v, --version`: Show version information
- `--verbose`: Enable debug mode
- `--model MODEL`: Specify AI model to use (default: gpt-4)
- `--api-key KEY`: Set OpenAI API key
- `--api-base URL`: Set custom API base URL
- `-n, --no-stream`: Disable streaming mode

## Environment Variables

You can set the following environment variables:
- `AI_API_KEY`: Your OpenAI API key
- `AI_MODEL`: AI model to use (default: gpt-4)
- `AI_API_BASE`: Custom API base URL

## Examples

1. Start the assistant:
```bash
ccc
```

2. Enable debug mode:
```bash
ccc --verbose
```

3. Use a specific model:
```bash
ccc --model gpt-3.5-turbo
```

4. Disable streaming output:
```bash
ccc -n
```

## License

MIT License 