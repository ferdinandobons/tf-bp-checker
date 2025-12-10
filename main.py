#!/usr/bin/env python3
"""
Terraform Best Practices Analyzer - Multi-Agent Orchestrator

A sophisticated multi-agent system that analyzes Terraform modules and provides
actionable recommendations for improving security, performance, compliance, and cost optimization.

## Architecture

This orchestrator coordinates three specialized agents:
1. Service Analyzer (Ollama) - Identifies AWS services in Terraform code
2. Resources Fetcher (Anthropic + MCP) - Queries Terraform Registry for best practices
3. Best Practices Advisor (Ollama) - Generates actionable recommendations

"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from pathlib import Path
import sys
import time

# Import specialized agents
from agents.service_analyzer_agent import analyze_aws_services
from agents.resources_fetcher_agent import create_resources_fetcher_agent, fetch_best_practices_resources
from agents.best_practices_advisor_agent import generate_recommendations


# Create the MCP client for Terraform at module level
terraform_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e", "TFE_ADDRESS=https://app.terraform.io",
            "-e", "TFE_TOKEN=''",
            "-e", "TRANSPORT_MODE=stdio",
            "hashicorp/terraform-mcp-server"
        ]
    )
))

ORCHESTRATOR_SYSTEM_PROMPT = """You are the Terraform Best Practices Orchestrator, coordinating specialized agents to analyze Terraform modules.

Your role is to:
1. Coordinate the analysis workflow across multiple specialized agents
2. Ensure each agent receives the correct input from previous steps
3. Present the final analysis in a clear, actionable format

Workflow:
1. First, use analyze_aws_services to identify AWS services in the Terraform code
2. Then, use the resources fetcher to get best practices from Terraform Registry
3. Finally, use generate_recommendations to create actionable suggestions

Always follow this sequence and ensure data flows correctly between agents."""


def find_terraform_files(directory: str) -> list:
    """Find all .tf files in the specified directory"""
    tf_files = []
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f"❌ Error: Directory '{directory}' does not exist")
        return []
    
    if not directory_path.is_dir():
        print(f"❌ Error: '{directory}' is not a directory")
        return []
    
    for file_path in directory_path.glob("*.tf"):
        tf_files.append(file_path)
    
    return sorted(tf_files)


def read_terraform_module(directory: str) -> tuple:
    """Read all Terraform files from a module directory"""
    tf_files = find_terraform_files(directory)
    
    if not tf_files:
        return {}, [], 0
    
    module_content = {}
    total_lines = 0
    
    for tf_file in tf_files:
        try:
            with open(tf_file, "r") as f:
                content = f.read()
                module_content[tf_file.name] = content
                total_lines += len(content.split('\n'))
        except Exception as e:
            print(f"⚠️  Warning: Could not read file '{tf_file}': {e}")

    return module_content, tf_files, total_lines


def format_module_content(module_content: dict) -> str:
    """Format the module content for display and analysis"""
    if not module_content:
        return "No Terraform code found."
    
    formatted = []
    for filename, content in module_content.items():
        formatted.append(f"## File: {filename}\n```hcl\n{content}\n```\n")
    return "\n".join(formatted)


def analyze_terraform_module(terraform_dir: str, terraform_tools: list, save_to_file: bool = True):
    """
    Main workflow for analyzing Terraform modules with multi-agent orchestration.
    
    Args:
        terraform_dir: Path to the Terraform module directory
        terraform_tools: List of tools from the Terraform MCP server
        save_to_file: Whether to save the output to a file (default: True)
        
    Returns:
        Dictionary containing analysis results
    """
    # Capture output for file saving
    output_lines = []
    
    def print_and_capture(message):
        """Print to console and capture for file output"""
        print(message)
        output_lines.append(message)
    
    print_and_capture("=" * 80)
    print_and_capture("🔍 TERRAFORM BEST PRACTICES ANALYZER")
    print_and_capture("=" * 80)
    print_and_capture(f"\n📂 Analyzing module: {terraform_dir}\n")
    
    # ========================================================================
    # STEP 1: Read Terraform Code
    # ========================================================================
    print_and_capture("=" * 80)
    print_and_capture("📖 STEP 1: Reading Terraform code...")
    print_and_capture("=" * 80)
    
    module_content, tf_files, total_lines = read_terraform_module(terraform_dir)
    
    if not tf_files:
        print_and_capture(f"\n❌ ERROR: No Terraform files found in '{terraform_dir}'")
        print_and_capture("Please provide a directory containing .tf files to analyze.")
        return None
    
    print_and_capture(f"\n📂 Module Directory: {terraform_dir}")
    print_and_capture(f"📄 Found {len(tf_files)} Terraform file(s) ({total_lines} lines total):")
    for tf_file in tf_files:
        print_and_capture(f"   - {tf_file.name}")
    
    formatted_content = format_module_content(module_content)
    
    # ========================================================================
    # STEP 2: Identify AWS Services (Agent 1 - Service Analyzer)
    # ========================================================================
    print_and_capture("\n" + "=" * 80)
    print_and_capture("🔍 STEP 2: Identifying AWS services...")
    print_and_capture("=" * 80)
    
    # Call the service analyzer agent (as a tool)
    aws_services = analyze_aws_services(formatted_content)
    print_and_capture(f"\n✅ Services identified: {aws_services}\n")
    
    # ========================================================================
    # STEP 3: Fetch Best Practices (Agent 2 - Resources Fetcher with MCP)
    # ========================================================================
    print_and_capture("\n" + "=" * 80)
    print_and_capture("🔧 STEP 3: Fetching best practices from Terraform Registry...")
    print_and_capture("=" * 80)
    print_and_capture(f"✅ Using {len(terraform_tools)} MCP tools from Terraform Registry\n")
    
    # Create the resources fetcher agent with MCP tools
    resources_fetcher = create_resources_fetcher_agent(terraform_tools)
    
    # Fetch best practices documentation
    best_practices_docs = fetch_best_practices_resources(resources_fetcher, aws_services)
    
    # ========================================================================
    # STEP 4: Generate Recommendations (Agent 3 - Best Practices Advisor)
    # ========================================================================
    print_and_capture("\n" + "=" * 80)
    print_and_capture("💡 STEP 4: Generating recommendations...")
    print_and_capture("=" * 80)
    
    # Call the advisor agent (as a tool)
    recommendations = generate_recommendations(
        formatted_content,
        aws_services,
        best_practices_docs
    )
    
    # ========================================================================
    # Present Final Results
    # ========================================================================
    print_and_capture("\n" + "=" * 80)
    print_and_capture("✨ BEST PRACTICES RECOMMENDATIONS")
    print_and_capture("=" * 80)
    print_and_capture(f"\n{recommendations}\n")
    
    # Save to file if requested
    output_file = None
    if save_to_file:
        # Generate filename with Unix timestamp
        timestamp = int(time.time())
        module_name = Path(terraform_dir).name
        output_file = f"terraform_analysis_{module_name}_{timestamp}.txt"
        
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(output_lines))
            print_and_capture(f"\n💾 Analysis saved to: {output_file}")
        except Exception as e:
            print(f"\n⚠️  Warning: Could not save to file: {e}")
    
    return {
        "module_directory": terraform_dir,
        "files_analyzed": [f.name for f in tf_files],
        "aws_services": aws_services,
        "best_practices_resources": best_practices_docs,
        "recommendations": recommendations,
        "output_file": output_file
    }


if __name__ == "__main__":
    print("\n🔍 Terraform Best Practices Analyzer - Multi-Agent System 🔍\n")
    
    # Get the Terraform module directory from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <terraform_module_directory>")
        print("\nExample: python main.py ./s3")
        print("\nThis tool will analyze your Terraform module and provide recommendations")
        print("for improving security, performance, compliance, and cost optimization.")
        sys.exit(1)
    
    terraform_directory = sys.argv[1]
    
    # Use the context manager to manage the MCP client lifecycle
    with terraform_mcp_client:
        # Get tools from the MCP server
        terraform_tools = terraform_mcp_client.list_tools_sync()
        print(f"✅ Connected to Terraform Registry MCP Server")
        print(f"✅ Loaded {len(terraform_tools)} MCP tools\n")
        
        # Execute the analysis workflow with multi-agent orchestration
        result = analyze_terraform_module(terraform_directory, terraform_tools)
        
        if result:
            print("\n" + "=" * 80)
            print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print(f"\n📊 Summary:")
            print(f"   - Module analyzed: {result['module_directory']}")
            print(f"   - Files reviewed: {len(result['files_analyzed'])}")
            print(f"   - AWS services found: {result['aws_services']}")
            if result.get('output_file'):
                print(f"   - Report saved to: {result['output_file']}")
            print(f"\n💡 Review the recommendations above to improve your Terraform module!")
        else:
            print("\n❌ Analysis failed. Please check the error messages above.")
            sys.exit(1)
