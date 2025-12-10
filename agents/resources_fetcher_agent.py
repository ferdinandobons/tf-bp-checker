"""
Resources Fetcher Agent for querying Terraform Registry.

This module provides the ResourcesFetcherAgent class that queries
the Terraform Registry for best practices documentation.
"""

from typing import List
from strands import Agent
from .base import AnthropicAgent
from .config import RESOURCES_FETCHER_SYSTEM_PROMPT


class ResourcesFetcherAgent(AnthropicAgent):
    """
    Agent specialized in fetching best practices from Terraform Registry.
    
    This agent uses Anthropic models with MCP tools to query the
    Terraform Registry and retrieve comprehensive documentation on
    resources and best practices.
    """
    
    def __init__(self, terraform_tools: List):
        """
        Initialize the Resources Fetcher Agent with MCP tools.
        
        Args:
            terraform_tools: List of tools from the Terraform MCP server
        """
        super().__init__(
            system_prompt=RESOURCES_FETCHER_SYSTEM_PROMPT,
            tools=terraform_tools
        )
    
    def analyze(self, aws_services: str) -> str:
        """
        Fetch best practices documentation for given AWS services.
        
        Args:
            aws_services: JSON string of AWS service names
            
        Returns:
            Comprehensive documentation on resources and best practices
        """
        return self.fetch_best_practices(aws_services)
    
    def fetch_best_practices(self, aws_services: str) -> str:
        """
        Fetch best practices documentation from Terraform Registry.
        
        Args:
            aws_services: JSON string of AWS service names
            
        Returns:
            Comprehensive documentation on resources and best practices
        """
        print("🔧 Fetching best practices from Terraform Registry...")
        print("   (This may take a minute as we query the registry for "
              "detailed information)")
        
        resources_prompt = f"""
For the following AWS services found in the code: {aws_services}

Use the available tools to:
1. Search the Terraform Registry for the AWS provider
2. For EACH service, get detailed documentation on:
   - All available resource types for that service
   - Resources that implement security best practices (encryption, \
access control, logging, etc.)
   - Resources for performance optimization (monitoring, caching, etc.)
   - Resources for compliance (versioning, backup, audit trails, etc.)
3. Get specific details on each resource including:
   - What the resource does
   - Why it's considered a best practice
   - Common configuration options

Be very thorough and use the tools extensively to gather complete \
information.
"""
        
        result = self.execute(resources_prompt)
        print("✅ Best practices documentation retrieved from Registry")
        return result


def create_resources_fetcher_agent(terraform_tools: List) -> Agent:
    """
    Create an agent that fetches Terraform resources and best practices.
    
    This function is provided for backward compatibility with the
    existing API.
    
    Args:
        terraform_tools: List of tools from the Terraform MCP server
        
    Returns:
        ResourcesFetcherAgent instance (wrapped as Agent)
    """
    return ResourcesFetcherAgent(terraform_tools)


def fetch_best_practices_resources(
    agent: ResourcesFetcherAgent,
    aws_services: str
) -> str:
    """
    Fetch best practices documentation from Terraform Registry.
    
    This function is provided for backward compatibility with the
    existing API.
    
    Args:
        agent: The resources fetcher agent
        aws_services: JSON string of AWS service names
        
    Returns:
        Comprehensive documentation on resources and best practices
    """
    try:
        return agent.fetch_best_practices(aws_services)
    except Exception as e:
        error_msg = f"Error fetching Terraform resources: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
