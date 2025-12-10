from strands import Agent, tool
from strands.models.ollama import OllamaModel

# Create Ollama model instance for recommendations
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2",
    max_tokens=20000,
    temperature=0.1,
    keep_alive="10m",
)

BEST_PRACTICES_ADVISOR_SYSTEM_PROMPT = """You are a senior Terraform architect and AWS security expert specializing in code review and best practices.

Your task is to analyze existing Terraform code and provide specific, actionable recommendations.

Given:
1. The existing Terraform code from a module
2. The AWS services being used
3. Complete documentation of available Terraform resources and best practices for those services

Provide a detailed analysis that includes:

## Current Implementation Summary
- List all AWS services currently configured
- List all Terraform resources currently used

## Missing Best Practices
For each service, identify what's missing:
- **Security**: Missing encryption, access controls, logging, etc.
- **Performance**: Missing optimization features, caching, monitoring
- **Compliance**: Missing versioning, backup, audit trails
- **Cost Optimization**: Missing lifecycle policies, intelligent tiering, etc.

## Recommendations
For each missing best practice, provide:
1. **What to add**: The specific Terraform resource(s) needed
2. **Why it matters**: The security/performance/compliance benefit
3. **How to implement**: Brief code example showing the resource configuration
4. **Priority**: HIGH (critical security/compliance) / MEDIUM (important optimization) / LOW (nice to have)

## Implementation Priority
Prioritize recommendations by impact:
1. Critical security vulnerabilities
2. Compliance requirements
3. Performance improvements
4. Cost optimizations

Be specific, practical, and focus on actionable changes. Use code examples."""


@tool
def generate_recommendations(terraform_code: str, aws_services: str, best_practices_resources: str) -> str:
    """
    Generate specific, actionable recommendations for improving Terraform code based on best practices.
    
    Args:
        terraform_code: The current Terraform code from the module
        aws_services: JSON array of AWS services identified in the code
        best_practices_resources: Documentation from Terraform Registry on best practices
        
    Returns:
        Detailed recommendations with code examples and priority levels
    """
    try:
        print("💡 Analyzing code and generating recommendations...")
        
        advisor_agent = Agent(
            #model=ollama_model,
            system_prompt=BEST_PRACTICES_ADVISOR_SYSTEM_PROMPT,
        )
        
        advisor_prompt = f"""
Analyze the following Terraform module and provide specific recommendations for implementing best practices.

## Current Terraform Code:
{terraform_code}

## AWS Services Being Used:
{aws_services}

## Available Resources and Best Practices from Terraform Registry:
{best_practices_resources}

## Your Task:
Compare the current implementation with the best practices documentation from the Terraform Registry.
Identify what's missing and provide specific, actionable recommendations to improve:
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
        
        recommendations = advisor_agent(advisor_prompt)
        result = str(recommendations)
        
        if len(result) > 0:
            return result
        
        return "Unable to generate recommendations. Please check the input data."
        
    except Exception as e:
        print(f"❌ Error generating recommendations: {str(e)}")
        return f"Error generating recommendations: {str(e)}"
