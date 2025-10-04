"""
Perplexity API package for interacting with Perplexity AI.
"""

from .perplexity_client import PerplexityClient, PerplexityModel, ask_perplexity
from .config import PerplexityConfig, default_config

__all__ = [
    'PerplexityClient',
    'PerplexityModel', 
    'ask_perplexity',
    'PerplexityConfig',
    'default_config'
]



