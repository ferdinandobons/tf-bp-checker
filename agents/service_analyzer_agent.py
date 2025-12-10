"""
Service Analyzer Agent for identifying AWS services in Terraform code.

This module provides the ServiceAnalyzerAgent class that analyzes
Terraform code and identifies all AWS services being used.
"""

from typing import Optional
from strands import tool
from .base import OllamaAgent
from .config import (
    SERVICE_ANALYZER_SYSTEM_PROMPT,
    OLLAMA_HOST,
    OLLAMA_MODEL_ID,
    OLLAMA_MAX_TOKENS,
    OLLAMA_TEMPERATURE,
    OLLAMA_KEEP_ALIVE
)


class ServiceAnalyzerAgent(OllamaAgent):
    """
    Agent specialized in analyzing Terraform code to identify AWS services.
    
    This agent uses Ollama to parse Terraform code and extract all
    AWS services referenced in resources, data sources, and modules.
    """
    
    def __init__(
        self,
        host: str = OLLAMA_HOST,
        model_id: str = OLLAMA_MODEL_ID,
        max_tokens: int = OLLAMA_MAX_TOKENS,
        temperature: float = OLLAMA_TEMPERATURE,
        keep_alive: str = OLLAMA_KEEP_ALIVE
    ):
        """
        Initialize the Service Analyzer Agent.
        
        Args:
            host: Ollama server host URL
            model_id: Model identifier
            max_tokens: Maximum tokens for generation
            temperature: Sampling temperature
            keep_alive: Keep-alive duration for model
        """
        super().__init__(
            system_prompt=SERVICE_ANALYZER_SYSTEM_PROMPT,
            host=host,
            model_id=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            keep_alive=keep_alive
        )
    
    def analyze(self, terraform_code: str) -> str:
        """
        Analyze Terraform code and identify all AWS services.
        
        Args:
            terraform_code: Complete Terraform code from all .tf files
            
        Returns:
            JSON array of AWS service names as a string
        """
        print("🔍 Analyzing Terraform code to identify AWS services...")
        
        analysis_prompt = f"""Analyze the following Terraform code and \
identify ALL AWS services being used:

{terraform_code}

Return a JSON array of AWS service names."""
        
        services_str = self.execute(analysis_prompt)
        
        if services_str and len(services_str) > 0:
            print(f"✅ AWS Services identified: {services_str}")
            return services_str
        
        print("⚠️  No services identified, returning default")
        return '["unknown"]'


# Global instance for backward compatibility
_service_analyzer_instance: Optional[ServiceAnalyzerAgent] = None


def get_service_analyzer() -> ServiceAnalyzerAgent:
    """
    Get or create the global ServiceAnalyzerAgent instance.
    
    Returns:
        ServiceAnalyzerAgent instance
    """
    global _service_analyzer_instance
    if _service_analyzer_instance is None:
        _service_analyzer_instance = ServiceAnalyzerAgent()
    return _service_analyzer_instance


@tool
def analyze_aws_services(terraform_code: str) -> str:
    """
    Analyze Terraform code and identify all AWS services being used.
    
    This is a tool wrapper for backward compatibility with the existing API.
    
    Args:
        terraform_code: Complete Terraform code from all .tf files
        
    Returns:
        JSON array of AWS service names as a string
    """
    try:
        analyzer = get_service_analyzer()
        return analyzer.analyze(terraform_code)
    except Exception as e:
        error_msg = f"Error identifying AWS services: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
