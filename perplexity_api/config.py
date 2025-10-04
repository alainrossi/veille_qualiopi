"""
Configuration module for Perplexity API client.
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class PerplexityConfig:
    """Configuration settings for Perplexity API client."""
    
    api_key: Optional[str] = None
    base_url: str = "https://api.perplexity.ai"
    default_model: str = "sonar"
    max_retries: int = 3
    timeout: int = 30
    
    def __post_init__(self):
        """Load configuration from environment variables if not provided."""
        if not self.api_key:
            self.api_key = os.getenv("PERPLEXITY_API_KEY")
        
        # Override with environment variables if they exist
        self.base_url = os.getenv("PERPLEXITY_BASE_URL", self.base_url)
        self.default_model = os.getenv("PERPLEXITY_DEFAULT_MODEL", self.default_model)
        
        # Parse numeric environment variables
        try:
            self.max_retries = int(os.getenv("PERPLEXITY_MAX_RETRIES", str(self.max_retries)))
            self.timeout = int(os.getenv("PERPLEXITY_TIMEOUT", str(self.timeout)))
        except ValueError:
            pass  # Keep default values if parsing fails
    
    @classmethod
    def from_env(cls) -> "PerplexityConfig":
        """Create configuration from environment variables."""
        return cls()
    
    def validate(self) -> bool:
        """Validate the configuration."""
        if not self.api_key:
            raise ValueError("API key is required. Set PERPLEXITY_API_KEY environment variable.")
        return True


# Default configuration instance
default_config = PerplexityConfig.from_env()
