"""Tests for the CLI tool using pytest"""

import subprocess
import pytest
import os

def test_cli_help_works():
    """Test that the CLI tool shows help message correctly"""
    result = subprocess.run(['ccc', '--help'], capture_output=True, text=True)
    assert result.returncode == 0
    assert 'usage: ccc' in result.stdout
    assert '--verbose' in result.stdout
    assert '--model' in result.stdout

def test_cli_version_works():
    """Test that the CLI tool shows version correctly"""
    result = subprocess.run(['ccc', '-v'], capture_output=True, text=True)
    assert result.returncode == 0
    assert 'CCC version' in result.stdout

@pytest.mark.skipif(not os.environ.get('AI_API_KEY'), reason="API key not set, skipping execution test")
def test_cli_execution():
    """Test that the CLI tool can execute with a simple command and exit
    
    This test requires AI_API_KEY to be set in environment variables.
    """
    # 使用输入管道模拟用户输入 "exit" 命令
    process = subprocess.Popen(
        ['ccc', '--no-stream'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input="exit\n")
    
    assert process.returncode == 0, f"Error: {stderr}"
    assert 'Goodbye' in stdout 