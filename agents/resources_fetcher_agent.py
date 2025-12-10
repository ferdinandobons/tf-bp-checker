from strands import Agent
from typing import List

RESOURCES_FETCHER_SYSTEM_PROMPT = """You are a Terraform specialist with access to the Terraform Registry tools via MCP.

IMPORTANT: You MUST use the available tools to search for up-to-date information from Terraform Registry.

Your task is to:
1. For each AWS service provided, use the tools to search the Terraform Registry
2. Get comprehensive documentation for ALL resources related to that service
3. Focus on resources that implement best practices for:
   - Security (encryption, access control, logging)
   - Performance (optimization, caching, monitoring)
   - Compliance (versioning, backup, audit trails)
   - Cost optimization

For each service, provide:
- The main resource types (e.g., aws_s3_bucket)
- All related security resources (e.g., aws_s3_bucket_public_access_block, aws_s3_bucket_server_side_encryption_configuration)
- Performance and monitoring resources
- Brief description of what each resource does and why it's a best practice

Be comprehensive and use the tools extensively to get accurate information."""


def create_resources_fetcher_agent(terraform_tools: List) -> Agent:
    """
    Create an agent that fetches Terraform resources and best practices from the Registry.
    
    This agent MUST use the default Anthropic model (not Ollama) because it needs
    to work with MCP tools from the Terraform Registry.
    
    Args:
        terraform_tools: List of tools from the Terraform MCP server
        
    Returns:
        An Agent configured to fetch resources from Terraform Registry
    """
    return Agent(
        system_prompt=RESOURCES_FETCHER_SYSTEM_PROMPT,
        tools=terraform_tools,
    )


def fetch_best_practices_resources(agent: Agent, aws_services: str) -> str:
    """
    Fetch best practices documentation from Terraform Registry for the given AWS services.
    
    Args:
        agent: The resources fetcher agent (must be created with MCP tools)
        aws_services: JSON string of AWS service names
        
    Returns:
        Comprehensive documentation on resources and best practices
    """
    try:
        print("🔧 Fetching best practices from Terraform Registry...")
        print("   (This may take a minute as we query the registry for detailed information)")
        
        resources_prompt = f"""
For the following AWS services found in the code: {aws_services}

Use the available tools to:
1. Search the Terraform Registry for the AWS provider
2. For EACH service, get detailed documentation on:
   - All available resource types for that service
   - Resources that implement security best practices (encryption, access control, logging, etc.)
   - Resources for performance optimization (monitoring, caching, etc.)
   - Resources for compliance (versioning, backup, audit trails, etc.)
3. Get specific details on each resource including:
   - What the resource does
   - Why it's considered a best practice
   - Common configuration options

Be very thorough and use the tools extensively to gather complete information.
"""
        
        best_practices = agent(resources_prompt)
        result = str(best_practices)
        
        print("✅ Best practices documentation retrieved from Registry")
        return result
        
    except Exception as e:
        print(f"❌ Error fetching resources: {str(e)}")
        return f"Error fetching Terraform resources: {str(e)}"
