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

## Development

### Installation for Development

```bash
# Clone the repository
git clone https://github.com/yourusername/ccc.git
cd ccc

# Install in development mode
pip install -e .
```

### Running Tests

The project uses pytest for testing. To run the tests:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run a specific test file
pytest tests/test_cli.py

# Run a specific test
pytest tests/test_cli.py::test_cli_help_works

# Run tests with coverage report
pytest --cov=ccc
```

### Building the Package

```bash
# Use the build script (recommended)
./build.sh
```

The build script automatically cleans up old files before building:
- Removes old build directories (`dist/`, `build/`)
- Cleans all egg-info directories
- Removes Python cache files (`__pycache__/`, `*.pyc`, etc.)
- Generates both wheel and source distribution packages

```bash
# Or build manually
python -m build
```

If building manually, you may want to clean old files first:
```bash
# Clean before building
rm -rf dist/ build/ *.egg-info/ __pycache__/ .pytest_cache/
find . -name "*.pyc" -delete
```

## License

MIT License 