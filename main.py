#!/usr/bin/env python3
"""
Terraform Best Practices Analyzer - Multi-Agent Orchestrator.

A sophisticated multi-agent system that analyzes Terraform modules and
provides actionable recommendations for improving security, performance,
compliance, and cost optimization.

Architecture:
This orchestrator coordinates three specialized agents:
1. Service Analyzer (Ollama) - Identifies AWS services in Terraform code
2. Resources Fetcher (Anthropic + MCP) - Queries Terraform Registry for
   best practices
3. Best Practices Advisor (Ollama) - Generates actionable recommendations
"""

import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional

from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

from agents.service_analyzer_agent import ServiceAnalyzerAgent
from agents.resources_fetcher_agent import ResourcesFetcherAgent
from agents.best_practices_advisor_agent import BestPracticesAdvisorAgent
from agents.config import MCP_COMMAND, MCP_ARGS


class TerraformFileReader:
    """
    Handles reading and parsing Terraform files from directories.
    
    This class encapsulates all file I/O operations for Terraform modules.
    """
    
    @staticmethod
    def find_terraform_files(directory: str) -> List[Path]:
        """
        Find all .tf files in the specified directory.
        
        Args:
            directory: Path to the directory to search
            
        Returns:
            Sorted list of Path objects for .tf files
        """
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"❌ Error: Directory '{directory}' does not exist")
            return []
        
        if not directory_path.is_dir():
            print(f"❌ Error: '{directory}' is not a directory")
            return []
        
        tf_files = list(directory_path.glob("*.tf"))
        return sorted(tf_files)
    
    @staticmethod
    def read_terraform_module(
        directory: str
    ) -> Tuple[Dict[str, str], List[Path], int]:
        """
        Read all Terraform files from a module directory.
        
        Args:
            directory: Path to the Terraform module directory
            
        Returns:
            Tuple of (module_content, tf_files, total_lines)
            - module_content: Dict mapping filename to file content
            - tf_files: List of Path objects for .tf files
            - total_lines: Total number of lines across all files
        """
        tf_files = TerraformFileReader.find_terraform_files(directory)
        
        if not tf_files:
            return {}, [], 0
        
        module_content = {}
        total_lines = 0
        
        for tf_file in tf_files:
            try:
                with open(tf_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    module_content[tf_file.name] = content
                    total_lines += len(content.split('\n'))
            except Exception as e:
                print(f"⚠️  Warning: Could not read file '{tf_file}': {e}")
        
        return module_content, tf_files, total_lines
    
    @staticmethod
    def format_module_content(module_content: Dict[str, str]) -> str:
        """
        Format the module content for display and analysis.
        
        Args:
            module_content: Dict mapping filename to file content
            
        Returns:
            Formatted string with all files and their contents
        """
        if not module_content:
            return "No Terraform code found."
        
        formatted = []
        for filename, content in module_content.items():
            formatted.append(
                f"## File: {filename}\n```hcl\n{content}\n```\n"
            )
        return "\n".join(formatted)


class ReportGenerator:
    """
    Handles output formatting and file generation for analysis results.
    
    This class manages all output operations including console printing
    and file saving.
    """
    
    def __init__(self):
        """Initialize the report generator."""
        self.output_lines: List[str] = []
    
    def print_and_capture(self, message: str) -> None:
        """
        Print to console and capture for file output.
        
        Args:
            message: The message to print and capture
        """
        print(message)
        self.output_lines.append(message)
    
    def save_to_file(
        self,
        module_name: str,
        timestamp: Optional[int] = None
    ) -> Optional[str]:
        """
        Save captured output to a file.
        
        Args:
            module_name: Name of the analyzed module
            timestamp: Unix timestamp (defaults to current time)
            
        Returns:
            Filename if successful, None otherwise
        """
        if timestamp is None:
            timestamp = int(time.time())
        
        output_file = f"terraform_analysis_{module_name}_{timestamp}.txt"
        
        try:
            with open(output_file, 'w', encoding="utf-8") as f:
                f.write('\n'.join(self.output_lines))
            self.print_and_capture(f"\n💾 Analysis saved to: {output_file}")
            return output_file
        except Exception as e:
            print(f"\n⚠️  Warning: Could not save to file: {e}")
            return None
    
    def get_output(self) -> str:
        """
        Get the complete captured output.
        
        Returns:
            All captured output as a single string
        """
        return '\n'.join(self.output_lines)


class MCPClientManager:
    """
    Manages the MCP client lifecycle for Terraform Registry access.
    
    This class encapsulates the MCP client connection and tool retrieval.
    """
    
    def __init__(self, command: str = MCP_COMMAND, args: List[str] = None):
        """
        Initialize the MCP client manager.
        
        Args:
            command: Command to run for MCP server
            args: Arguments for the MCP server command
        """
        self.command = command
        self.args = args or MCP_ARGS
        self.client = self._create_client()
    
    def _create_client(self) -> MCPClient:
        """
        Create the MCP client instance.
        
        Returns:
            Configured MCPClient instance
        """
        return MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command=self.command,
                args=self.args
            )
        ))
    
    def __enter__(self):
        """Enter context manager."""
        self.client.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        return self.client.__exit__(exc_type, exc_val, exc_tb)
    
    def list_tools(self) -> List:
        """
        Get the list of available tools from the MCP server.
        
        Returns:
            List of available tools
        """
        return self.client.list_tools_sync()


class TerraformAnalyzer:
    """
    Main orchestrator for Terraform module analysis.
    
    This class coordinates the multi-agent analysis workflow and manages
    the interaction between specialized agents.
    """
    
    def __init__(self, terraform_tools: List):
        """
        Initialize the Terraform analyzer with MCP tools.
        
        Args:
            terraform_tools: List of tools from the Terraform MCP server
        """
        self.terraform_tools = terraform_tools
        self.file_reader = TerraformFileReader()
        self.report_generator = ReportGenerator()
        
        # Initialize specialized agents
        self.service_analyzer = ServiceAnalyzerAgent()
        self.resources_fetcher = ResourcesFetcherAgent(terraform_tools)
        self.advisor = BestPracticesAdvisorAgent()
    
    def analyze_module(
        self,
        terraform_dir: str,
        save_to_file: bool = True
    ) -> Optional[Dict]:
        """
        Execute the complete analysis workflow for a Terraform module.
        
        Args:
            terraform_dir: Path to the Terraform module directory
            save_to_file: Whether to save output to a file
            
        Returns:
            Dictionary containing analysis results, or None if failed
        """
        rg = self.report_generator
        
        # Header
        rg.print_and_capture("=" * 80)
        rg.print_and_capture("🔍 TERRAFORM BEST PRACTICES ANALYZER")
        rg.print_and_capture("=" * 80)
        rg.print_and_capture(f"\n📂 Analyzing module: {terraform_dir}\n")
        
        # Step 1: Read Terraform code
        module_content, tf_files, total_lines = self._read_code(
            terraform_dir, rg
        )
        if not tf_files:
            return None
        
        formatted_content = self.file_reader.format_module_content(
            module_content
        )
        
        # Step 2: Identify AWS services
        aws_services = self._identify_services(formatted_content, rg)
        
        # Step 3: Fetch best practices
        best_practices_docs = self._fetch_best_practices(aws_services, rg)
        
        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(
            formatted_content, aws_services, best_practices_docs, rg
        )
        
        # Present final results
        self._present_results(recommendations, rg)
        
        # Save to file if requested
        output_file = None
        if save_to_file:
            module_name = Path(terraform_dir).name
            output_file = rg.save_to_file(module_name)
        
        return {
            "module_directory": terraform_dir,
            "files_analyzed": [f.name for f in tf_files],
            "aws_services": aws_services,
            "best_practices_resources": best_practices_docs,
            "recommendations": recommendations,
            "output_file": output_file
        }
    
    def _read_code(
        self,
        terraform_dir: str,
        rg: ReportGenerator
    ) -> Tuple[Dict[str, str], List[Path], int]:
        """
        Read Terraform code from directory.
        
        Args:
            terraform_dir: Path to the Terraform module directory
            rg: ReportGenerator instance for output
            
        Returns:
            Tuple of (module_content, tf_files, total_lines)
        """
        rg.print_and_capture("=" * 80)
        rg.print_and_capture("📖 STEP 1: Reading Terraform code...")
        rg.print_and_capture("=" * 80)
        
        module_content, tf_files, total_lines = (
            self.file_reader.read_terraform_module(terraform_dir)
        )
        
        if not tf_files:
            rg.print_and_capture(
                f"\n❌ ERROR: No Terraform files found in '{terraform_dir}'"
            )
            rg.print_and_capture(
                "Please provide a directory containing .tf files to analyze."
            )
            return {}, [], 0
        
        rg.print_and_capture(f"\n📂 Module Directory: {terraform_dir}")
        rg.print_and_capture(
            f"📄 Found {len(tf_files)} Terraform file(s) "
            f"({total_lines} lines total):"
        )
        for tf_file in tf_files:
            rg.print_and_capture(f"   - {tf_file.name}")
        
        return module_content, tf_files, total_lines
    
    def _identify_services(
        self,
        formatted_content: str,
        rg: ReportGenerator
    ) -> str:
        """
        Identify AWS services in the Terraform code.
        
        Args:
            formatted_content: Formatted Terraform code
            rg: ReportGenerator instance for output
            
        Returns:
            JSON string of identified AWS services
        """
        rg.print_and_capture("\n" + "=" * 80)
        rg.print_and_capture("🔍 STEP 2: Identifying AWS services...")
        rg.print_and_capture("=" * 80)
        
        aws_services = self.service_analyzer.analyze(formatted_content)
        rg.print_and_capture(f"\n✅ Services identified: {aws_services}\n")
        
        return aws_services
    
    def _fetch_best_practices(
        self,
        aws_services: str,
        rg: ReportGenerator
    ) -> str:
        """
        Fetch best practices from Terraform Registry.
        
        Args:
            aws_services: JSON string of AWS service names
            rg: ReportGenerator instance for output
            
        Returns:
            Best practices documentation
        """
        rg.print_and_capture("\n" + "=" * 80)
        rg.print_and_capture(
            "🔧 STEP 3: Fetching best practices from Terraform Registry..."
        )
        rg.print_and_capture("=" * 80)
        rg.print_and_capture(
            f"✅ Using {len(self.terraform_tools)} MCP tools from "
            "Terraform Registry\n"
        )
        
        best_practices_docs = self.resources_fetcher.fetch_best_practices(
            aws_services
        )
        
        return best_practices_docs
    
    def _generate_recommendations(
        self,
        formatted_content: str,
        aws_services: str,
        best_practices_docs: str,
        rg: ReportGenerator
    ) -> str:
        """
        Generate actionable recommendations.
        
        Args:
            formatted_content: Formatted Terraform code
            aws_services: JSON string of AWS service names
            best_practices_docs: Best practices documentation
            rg: ReportGenerator instance for output
            
        Returns:
            Recommendations text
        """
        rg.print_and_capture("\n" + "=" * 80)
        rg.print_and_capture("💡 STEP 4: Generating recommendations...")
        rg.print_and_capture("=" * 80)
        
        recommendations = self.advisor.generate_recommendations(
            formatted_content,
            aws_services,
            best_practices_docs
        )
        
        return recommendations
    
    def _present_results(
        self,
        recommendations: str,
        rg: ReportGenerator
    ) -> None:
        """
        Present final analysis results.
        
        Args:
            recommendations: Generated recommendations
            rg: ReportGenerator instance for output
        """
        rg.print_and_capture("\n" + "=" * 80)
        rg.print_and_capture("✨ BEST PRACTICES RECOMMENDATIONS")
        rg.print_and_capture("=" * 80)
        rg.print_and_capture(f"\n{recommendations}\n")


def main() -> int:
    """
    Main entry point for the Terraform Best Practices Analyzer.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print("\n🔍 Terraform Best Practices Analyzer - "
          "Multi-Agent System 🔍\n")
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <terraform_module_directory>")
        print("\nExample: python main.py ./s3")
        print("\nThis tool will analyze your Terraform module and provide "
              "recommendations")
        print("for improving security, performance, compliance, and cost "
              "optimization.")
        return 1
    
    terraform_directory = sys.argv[1]
    
    # Initialize MCP client manager and run analysis
    mcp_manager = MCPClientManager()
    
    with mcp_manager:
        # Get tools from the MCP server
        terraform_tools = mcp_manager.list_tools()
        print("✅ Connected to Terraform Registry MCP Server")
        print(f"✅ Loaded {len(terraform_tools)} MCP tools\n")
        
        # Create analyzer and execute workflow
        analyzer = TerraformAnalyzer(terraform_tools)
        result = analyzer.analyze_module(terraform_directory)
        
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
            print("\n💡 Review the recommendations above to improve your "
                  "Terraform module!")
            return 0
        else:
            print("\n❌ Analysis failed. Please check the error messages "
                  "above.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
