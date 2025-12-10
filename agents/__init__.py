"""
Terraform Best Practices Analyzer - Multi-Agent System

This package contains specialized agents for analyzing Terraform modules:
- service-analyzer-agent: Identifies AWS services in Terraform code
- resources-fetcher-agent: Queries Terraform Registry for best practices
- best-practices-advisor-agent: Generates actionable recommendations
"""

from .service_analyzer_agent import analyze_aws_services
from .best_practices_advisor_agent import generate_recommendations

__all__ = [
    'analyze_aws_services',
    'generate_recommendations',
]
