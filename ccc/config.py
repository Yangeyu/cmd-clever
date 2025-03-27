"""Configuration management for CCC"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration settings for CCC"""
    api_key: str = os.getenv("AI_API_KEY", "")
    model: str = os.getenv("AI_MODEL", "gpt-4")
    api_base: str = os.getenv("AI_API_BASE", "https://api.openai.com/v1")
    debug: bool = False
    
    @classmethod
    def from_args(cls, args) -> 'Config':
        """Create config from command line arguments"""
        return cls(
            api_key=args.api_key or os.getenv("AI_API_KEY", ""),
            model=args.model or os.getenv("AI_MODEL", "gpt-4"),
            api_base=args.api_base or os.getenv("AI_API_BASE", "https://api.openai.com/v1"),
            debug=args.verbose,
        ) 