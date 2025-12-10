"""
Terraform Best Practices Analyzer - Multi-Agent System.

This package contains specialized agents for analyzing Terraform modules:
- ServiceAnalyzerAgent: Identifies AWS services in Terraform code
- ResourcesFetcherAgent: Queries Terraform Registry for best practices
- BestPracticesAdvisorAgent: Generates actionable recommendations

The package also provides base classes and configuration for extending
the system with additional agents.
"""

# Import agent classes
from .service_analyzer_agent import (
    ServiceAnalyzerAgent,
    analyze_aws_services,
    get_service_analyzer
)
from .resources_fetcher_agent import (
    ResourcesFetcherAgent,
    create_resources_fetcher_agent,
    fetch_best_practices_resources
)
from .best_practices_advisor_agent import (
    BestPracticesAdvisorAgent,
    generate_recommendations,
    get_advisor
)

# Import base classes
from .base import (
    BaseAgent,
    OllamaAgent,
    AnthropicAgent,
    ToolCapableAgent
)

# Import configuration
from . import config

__all__ = [
    # Agent classes
    'ServiceAnalyzerAgent',
    'ResourcesFetcherAgent',
    'BestPracticesAdvisorAgent',
    
    # Base classes
    'BaseAgent',
    'OllamaAgent',
    'AnthropicAgent',
    'ToolCapableAgent',
    
    # Tool functions (backward compatibility)
    'analyze_aws_services',
    'generate_recommendations',
    
    # Helper functions
    'get_service_analyzer',
    'get_advisor',
    'create_resources_fetcher_agent',
    'fetch_best_practices_resources',
    
    # Configuration module
    'config',
]

__version__ = '1.0.0'
__author__ = 'Terraform Best Practices Analyzer Team'
