"""
Best Practices Advisor Agent for generating recommendations.

This module provides the BestPracticesAdvisorAgent class that analyzes
Terraform code and generates actionable recommendations.
"""

from typing import Optional
from strands import tool
from .base import OllamaAgent
from .config import (
    BEST_PRACTICES_ADVISOR_SYSTEM_PROMPT,
    OLLAMA_HOST,
    OLLAMA_MODEL_ID,
    OLLAMA_MAX_TOKENS,
    OLLAMA_TEMPERATURE,
    OLLAMA_KEEP_ALIVE
)


class BestPracticesAdvisorAgent(OllamaAgent):
    """
    Agent specialized in generating best practices recommendations.
    
    This agent analyzes Terraform code against best practices documentation
    and generates specific, actionable recommendations for improvements.
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
        Initialize the Best Practices Advisor Agent.
        
        Args:
            host: Ollama server host URL
            model_id: Model identifier
            max_tokens: Maximum tokens for generation
            temperature: Sampling temperature
            keep_alive: Keep-alive duration for model
        """
        super().__init__(
            system_prompt=BEST_PRACTICES_ADVISOR_SYSTEM_PROMPT,
            host=host,
            model_id=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            keep_alive=keep_alive
        )
    
    def analyze(
        self,
        terraform_code: str,
        aws_services: str,
        best_practices_resources: str
    ) -> str:
        """
        Generate recommendations for improving Terraform code.
        
        Args:
            terraform_code: Current Terraform code from the module
            aws_services: JSON array of AWS services identified
            best_practices_resources: Documentation from Terraform Registry
            
        Returns:
            Detailed recommendations with code examples and priorities
        """
        return self.generate_recommendations(
            terraform_code,
            aws_services,
            best_practices_resources
        )
    
    def generate_recommendations(
        self,
        terraform_code: str,
        aws_services: str,
        best_practices_resources: str
    ) -> str:
        """
        Generate specific, actionable recommendations.
        
        Args:
            terraform_code: Current Terraform code from the module
            aws_services: JSON array of AWS services identified
            best_practices_resources: Documentation from Terraform Registry
            
        Returns:
            Detailed recommendations with code examples and priorities
        """
        print("💡 Analyzing code and generating recommendations...")
        
        advisor_prompt = f"""
Analyze the following Terraform module and provide specific recommendations \
for implementing best practices.

## Current Terraform Code:
{terraform_code}

## AWS Services Being Used:
{aws_services}

## Available Resources and Best Practices from Terraform Registry:
{best_practices_resources}

## Your Task:
Compare the current implementation with the best practices documentation \
from the Terraform Registry.
Identify what's missing and provide specific, actionable recommendations \
to improve:
- Security (encryption, access control, logging)
- Performance (monitoring, optimization)
- Compliance (versioning, backup, audit)
- Cost optimization

For each recommendation:
1. Clearly state what resource/configuration is missing
2. Explain why it's important (security, performance, compliance, cost)
3. Provide a specific code example showing how to add it
4. Assign a priority level (HIGH/MEDIUM/LOW)

Focus on practical, implementable changes that will have real impact.
"""
        
        recommendations = self.execute(advisor_prompt)
        
        if recommendations and len(recommendations) > 0:
            return recommendations
        
        return "Unable to generate recommendations. Please check input data."


# Global instance for backward compatibility
_advisor_instance: Optional[BestPracticesAdvisorAgent] = None


def get_advisor() -> BestPracticesAdvisorAgent:
    """
    Get or create the global BestPracticesAdvisorAgent instance.
    
    Returns:
        BestPracticesAdvisorAgent instance
    """
    global _advisor_instance
    if _advisor_instance is None:
        _advisor_instance = BestPracticesAdvisorAgent()
    return _advisor_instance


@tool
def generate_recommendations(
    terraform_code: str,
    aws_services: str,
    best_practices_resources: str
) -> str:
    """
    Generate recommendations for improving Terraform code.
    
    This is a tool wrapper for backward compatibility with the existing API.
    
    Args:
        terraform_code: Current Terraform code from the module
        aws_services: JSON array of AWS services identified
        best_practices_resources: Documentation from Terraform Registry
        
    Returns:
        Detailed recommendations with code examples and priorities
    """
    try:
        advisor = get_advisor()
        return advisor.generate_recommendations(
            terraform_code,
            aws_services,
            best_practices_resources
        )
    except Exception as e:
        error_msg = f"Error generating recommendations: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
