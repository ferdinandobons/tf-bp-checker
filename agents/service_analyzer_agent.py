from strands import Agent, tool
from strands.models.ollama import OllamaModel

# Create Ollama model instance for service analysis
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2",
    max_tokens=20000,
    temperature=0.1,
    keep_alive="10m",
)

SERVICE_ANALYZER_SYSTEM_PROMPT = """You are an AWS and Terraform expert specializing in analyzing Terraform code.

Your task is to analyze Terraform code and identify ALL AWS services being used.

Look for:
- Resource declarations (e.g., resource "aws_s3_bucket", resource "aws_iam_role")
- Data sources (e.g., data "aws_ami", data "aws_vpc")
- Module calls that might use AWS resources
- Any AWS service references

Return ONLY a JSON array of AWS service names (without the "aws_" prefix), for example:
["s3", "iam", "kms", "cloudwatch", "ec2", "vpc"]

Be thorough and include all services you find. Return only the JSON array, nothing else."""


@tool
def analyze_aws_services(terraform_code: str) -> str:
    """
    Analyze Terraform code and identify all AWS services being used.
    
    Args:
        terraform_code: The complete Terraform code from all .tf files in the module
        
    Returns:
        A JSON array of AWS service names found in the code
    """
    try:
        print("🔍 Analyzing Terraform code to identify AWS services...")
        
        service_analyzer = Agent(
            #model=ollama_model,
            system_prompt=SERVICE_ANALYZER_SYSTEM_PROMPT,
        )
        
        analysis_prompt = f"""Analyze the following Terraform code and identify ALL AWS services being used:

{terraform_code}

Return a JSON array of AWS service names."""
        
        services = service_analyzer(analysis_prompt)
        services_str = str(services)
        
        if len(services_str) > 0:
            print(f"✅ AWS Services identified: {services_str}")
            return services_str
        
        return '["unknown"]'
        
    except Exception as e:
        print(f"❌ Error analyzing services: {str(e)}")
        return f"Error identifying AWS services: {str(e)}"
