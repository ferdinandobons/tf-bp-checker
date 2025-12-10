# Terraform Best Practices Analyzer

🔍 **AI-powered Terraform module analyzer** that identifies missing best practices and provides actionable recommendations for improving security, performance, compliance, and cost optimization.

## ✨ Overview

This tool uses a **multi-agent architecture** with Strands Agents to analyze your existing Terraform code and suggest improvements based on official Terraform Registry documentation and AWS best practices.

### How It Works

```
Your Terraform Code → 4-Step Analysis → Detailed Recommendations
```

#### 4-Step Multi-Agent Workflow

1. **📖 Read Terraform Code** - Scans all `.tf` files in your module
2. **🔍 Identify AWS Services** - Ollama agent analyzes code to detect all AWS services
3. **🔧 Fetch Best Practices** - MCP agent queries Terraform Registry for official documentation
4. **💡 Generate Recommendations** - Ollama agent compares your code with best practices and provides specific, actionable suggestions

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# Or install manually:
# pip install 'strands-agents[ollama]' strands-agents-tools mcp

# 2. Pull Docker image for Terraform MCP Server
docker pull hashicorp/terraform-mcp-server

# 3. Install Ollama model (7B+ recommended)
ollama pull llama3.2
```

### Usage

```bash
python main.py <terraform_module_directory>
```

**Example:**
```bash
python main.py ./s3
```

The analysis output is automatically saved to a file with format:
```
terraform_analysis_<module_name>_<unix_timestamp>.txt
```

For example:
```
terraform_analysis_s3_1702218345.txt
```

## 📊 What You Get

The tool generates a comprehensive analysis report with:

### ✅ Current Implementation Summary
- List of all AWS services currently configured
- Inventory of Terraform resources in use

### ❌ Missing Best Practices
Categorized by:
- **Security**: Missing encryption, access controls, logging
- **Performance**: Missing monitoring, optimization features
- **Compliance**: Missing versioning, backup, audit trails
- **Cost Optimization**: Missing lifecycle policies, intelligent tiering

### 💡 Actionable Recommendations
For each recommendation:
- **What to add**: Specific Terraform resource(s) needed
- **Why it matters**: Security/performance/compliance benefit
- **How to implement**: Code example showing the configuration
- **Priority level**: HIGH / MEDIUM / LOW

## 🎯 Example Output

```bash
$ python main.py ./s3

================================================================================
🔍 TERRAFORM BEST PRACTICES ANALYZER
================================================================================

📂 Analyzing module: ./s3

================================================================================
📖 STEP 1: Reading Terraform code...
================================================================================

📂 Module Directory: ./s3
📄 Found 1 Terraform file(s) (28 lines total):
   - s3.tf

================================================================================
🔍 STEP 2: Identifying AWS services in the code...
================================================================================

✅ AWS Services identified in code:
["s3", "kms"]

================================================================================
🔧 STEP 3: Fetching best practices from Terraform Registry...
================================================================================

✅ Using 34 MCP tools from Terraform Registry
⏳ Fetching comprehensive resource documentation...

✅ Best practices documentation retrieved from Registry

================================================================================
💡 STEP 4: Analyzing code and generating recommendations...
================================================================================

================================================================================
✨ BEST PRACTICES RECOMMENDATIONS
================================================================================

## Current Implementation Summary

Your S3 module currently implements:
- aws_s3_bucket (main bucket resource)
- aws_s3_bucket_versioning (enabled)
- aws_s3_bucket_public_access_block (configured)

## Missing Best Practices

### 🔐 Security (HIGH Priority)

**1. Server-Side Encryption**
- Missing: aws_s3_bucket_server_side_encryption_configuration
- Why: Encrypts data at rest, protecting against unauthorized access
- How to implement:

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encryption" {
  bucket = aws_s3_bucket.my_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.mykey.arn
    }
  }
}

**2. Bucket Logging**
- Missing: aws_s3_bucket_logging
- Why: Audit trail for compliance and security monitoring
- Priority: HIGH

### ⚡ Performance (MEDIUM Priority)

**3. CloudWatch Metrics**
- Missing: aws_s3_bucket_metric
- Why: Monitor bucket performance and usage patterns
...

🎉 ANALYSIS COMPLETED SUCCESSFULLY!
```

## 🏗️ Architecture

### Object-Oriented Multi-Agent System

The tool uses a **modern OOP architecture** with specialized agents coordinated by an orchestrator class:

```
TerraformAnalyzer (Orchestrator)
    ↓
    ├─→ ServiceAnalyzerAgent (Agent 1)
    │   └─→ Identifies AWS services in code
    │
    ├─→ ResourcesFetcherAgent (Agent 2)
    │   └─→ Queries Terraform Registry via MCP
    │
    └─→ BestPracticesAdvisorAgent (Agent 3)
        └─→ Generates actionable recommendations
```

### Class Structure

| Class | File | Base Class | Purpose |
|-------|------|------------|---------|
| **TerraformAnalyzer** | `main.py` | - | Main orchestrator coordinating all agents |
| **ServiceAnalyzerAgent** | `service_analyzer_agent.py` | OllamaAgent | Identifies AWS services in Terraform code |
| **ResourcesFetcherAgent** | `resources_fetcher_agent.py` | AnthropicAgent | Queries Terraform Registry for best practices |
| **BestPracticesAdvisorAgent** | `best_practices_advisor_agent.py` | OllamaAgent | Generates recommendations |
| **BaseAgent** | `base.py` | ABC | Abstract base class for all agents |
| **OllamaAgent** | `base.py` | BaseAgent | Base class for Ollama-powered agents |
| **AnthropicAgent** | `base.py` | BaseAgent | Base class for Anthropic-powered agents |
| **TerraformFileReader** | `main.py` | - | Handles file I/O operations |
| **ReportGenerator** | `main.py` | - | Manages output formatting and saving |
| **MCPClientManager** | `main.py` | - | Manages MCP client lifecycle |

### Why This OOP Design?

- **Proper encapsulation**: Each class has clear responsibilities and internal state
- **Inheritance hierarchy**: Base classes provide common functionality
- **Single Responsibility Principle**: Each class does one thing well
- **Dependency injection**: Agents receive their dependencies through constructors
- **Easy to test**: Classes can be tested independently with mocks
- **PEP8 compliant**: Follows Python style guidelines
- **Extensible**: Easy to add new agent types or functionality
- **Reusable components**: All classes can be imported and used independently

## 📋 Requirements

### Essential
- ✅ **Python 3.10+** with required packages
- ✅ **Docker** running (for MCP server)
- ✅ **Ollama** with 7B+ model

### Recommended Models

| Model | Size | Analysis Quality | Speed | Recommendation |
|-------|------|------------------|-------|----------------|
| llama3.2 | 7B | ✅ Good | 🚀 Fast | ✅ **Recommended** |
| llama3.1:8b | 8B | ✅ Good | 🚀 Fast | ✅ **Recommended** |
| qwen2.5:7b | 7B | ✅ Good | 🚀 Fast | ✅ Good alternative |
| mixtral:8x7b | 47B | ✅ Excellent | 🐢 Slow | ⚡ Best quality |

⚠️ **Note**: 3B models are NOT recommended - they struggle with complex analysis.

## 🔧 Configuration

### Using Different Models

The tool uses configuration constants in `agents/config.py`. To change models:

**Edit Global Configuration:**
```python
# In agents/config.py
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL_ID = "llama3.2"
OLLAMA_MAX_TOKENS = 20000
OLLAMA_TEMPERATURE = 0.1
OLLAMA_KEEP_ALIVE = "10m"
```

**Or Create Custom Agents:**
```python
from agents import ServiceAnalyzerAgent

# Custom agent instance with different model
analyzer = ServiceAnalyzerAgent(
    model_id="mixtral:8x7b",
    max_tokens=30000,
    temperature=0.05
)
```

### Programmatic Usage

The OOP design allows you to use the system programmatically:

```python
from main import TerraformAnalyzer, MCPClientManager

# Initialize MCP client
with MCPClientManager() as mcp:
    tools = mcp.list_tools()
    
    # Create analyzer
    analyzer = TerraformAnalyzer(tools)
    
    # Run analysis
    result = analyzer.analyze_module("./my-terraform-module")
    
    print(f"Services found: {result['aws_services']}")
    print(f"Recommendations: {result['recommendations']}")
```

### Extending the System

Thanks to the OOP architecture, you can easily extend the system:

**Create a Custom Agent:**
```python
# Create agents/custom_agent.py
from agents.base import OllamaAgent

class CustomAnalyzerAgent(OllamaAgent):
    """Custom agent for specialized analysis."""
    
    def __init__(self):
        super().__init__(
            system_prompt="Your custom prompt here...",
            model_id="llama3.2"
        )
    
    def analyze(self, data: str) -> str:
        """Perform custom analysis."""
        prompt = f"Analyze: {data}"
        return self.execute(prompt)
```

**Use Inheritance for Common Functionality:**
```python
from agents.base import BaseAgent

class MyAgent(BaseAgent):
    """Your custom agent."""
    
    def analyze(self, *args, **kwargs) -> str:
        # Implement your logic
        return self.execute("your prompt")
```

**Customize the Orchestrator:**
```python
from main import TerraformAnalyzer

class CustomAnalyzer(TerraformAnalyzer):
    """Custom orchestrator with additional steps."""
    
    def analyze_module(self, terraform_dir: str, **kwargs):
        # Add pre-processing
        result = super().analyze_module(terraform_dir, **kwargs)
        # Add post-processing
        return result
```

## 📁 Project Structure

### Tool Structure

```
tf-bp-checker/
├── main.py                              # Main orchestrator with OOP classes
│   ├── TerraformAnalyzer               # Main analysis orchestrator
│   ├── TerraformFileReader             # File I/O operations
│   ├── ReportGenerator                 # Output formatting and saving
│   └── MCPClientManager                # MCP client lifecycle management
├── agents/                              # Multi-agent system package
│   ├── __init__.py                     # Package exports
│   ├── base.py                         # Base classes for all agents
│   │   ├── BaseAgent                   # Abstract base class
│   │   ├── OllamaAgent                 # Ollama agent base
│   │   └── AnthropicAgent              # Anthropic agent base
│   ├── config.py                       # Configuration constants
│   ├── service_analyzer_agent.py       # ServiceAnalyzerAgent class
│   ├── resources_fetcher_agent.py      # ResourcesFetcherAgent class
│   └── best_practices_advisor_agent.py # BestPracticesAdvisorAgent class
├── requirements.txt                     # Python dependencies
├── README.md                            # Documentation
└── s3/                                  # Example Terraform module
    └── s3.tf
```

### Example Terraform Module Structure

```
my-terraform-project/
├── s3/
│   ├── s3.tf
│   ├── variables.tf
│   └── outputs.tf
├── vpc/
│   ├── main.tf
│   ├── subnets.tf
│   └── security-groups.tf
└── ec2/
    ├── instances.tf
    └── iam.tf
```

Analyze each module:
```bash
python main.py ./s3
python main.py ./vpc
python main.py ./ec2
```

## 🎓 Use Cases

### Security Audit
```bash
python main.py ./production-infrastructure
```
Identifies missing encryption, access controls, logging, and security groups.

### Compliance Check
```bash
python main.py ./regulated-workload
```
Checks for versioning, backup, audit trails, and compliance-required features.

### Cost Optimization
```bash
python main.py ./data-storage
```
Suggests lifecycle policies, intelligent tiering, and storage optimization.

### Performance Review
```bash
python main.py ./high-traffic-app
```
Recommends monitoring, metrics, acceleration, and optimization features.

## 📄 Output Files

The tool automatically saves the complete analysis to a timestamped file for future reference:

**File naming format:**
```
terraform_analysis_<module_name>_<unix_timestamp>.txt
```

**Benefits:**
- 📝 Keep historical records of your module's evolution
- 🔄 Compare analyses over time as you implement recommendations
- 📤 Share reports with your team easily
- 📊 Track improvements between analysis runs

**Example files:**
```
terraform_analysis_s3_1702218345.txt
terraform_analysis_vpc_1702218567.txt
terraform_analysis_ec2_1702218789.txt
```

**Tips:**
- Files are saved in the same directory where you run the command
- Compare different timestamps to see your progress
- Add these files to `.gitignore` (already configured)

## 🐛 Troubleshooting

### "No Terraform files found"
**Cause:** Directory doesn't contain `.tf` files

**Solution:** 
- Verify the directory path is correct
- Ensure files have `.tf` extension
- Check you're not in a subdirectory

### Analysis gets stuck at Step 3
**Cause:** MCP server connection issue

**Solution:**
```bash
# Check Docker is running
docker ps

# Pull the image again
docker pull hashicorp/terraform-mcp-server

# Restart Docker if needed
```

### Agent returns generic advice instead of specific recommendations
**Cause:** Model too small or wrong model type

**Solution:**
- Use 7B+ model: `ollama pull llama3.2`
- Check Ollama is running: `ollama list`
- Verify model in code matches installed model

### Slow performance
**Causes:** Large model, complex module, or first run

**Solutions:**
- Keep Docker running to avoid startup time
- Use faster 7B model instead of 47B
- Increase `keep_alive` to 30m for multiple runs
- Simplify the module into smaller components

## 💡 Best Practices for Using This Tool

1. **Start small**: Analyze one module at a time
2. **Prioritize**: Focus on HIGH priority recommendations first
3. **Iterate**: Apply changes, then re-analyze to verify
4. **Document**: Keep track of which recommendations you've implemented
5. **Learn**: Use the tool as a learning resource for Terraform best practices

## 🔍 What Gets Analyzed

The tool examines all `.tf` files for:
- ✅ Resource definitions and configurations
- ✅ Data sources
- ✅ Variables and outputs
- ✅ Provider settings
- ✅ Module calls
- ✅ Terraform settings

It then compares against best practices for:
- 🔐 **Security**: Encryption, access control, network security
- ⚡ **Performance**: Monitoring, caching, optimization
- 📋 **Compliance**: Versioning, logging, audit trails
- 💰 **Cost**: Lifecycle policies, tiering, resource optimization

## 📚 Additional Resources

- [Strands Agents Documentation](https://strandsagents.com)
- [Terraform Registry](https://registry.terraform.io)
- [AWS Best Practices](https://aws.amazon.com/architecture/well-architected/)
- [Terraform MCP Server](https://github.com/hashicorp/terraform-mcp-server)
- [Ollama Models](https://ollama.com/library)
- [Model Context Protocol](https://modelcontextprotocol.io)

## 🤝 Contributing

This tool is designed to be extensible. You can:
- Add support for other cloud providers (Azure, GCP)
- Customize the system prompts for different focus areas
- Add new analysis agents for specific compliance frameworks
- Integrate with CI/CD pipelines

## 📄 License

This project is open source and available under standard licensing terms.

---

**Built with:**
- [Strands Agents](https://strandsagents.com) - Multi-agent orchestration framework
- [Ollama](https://ollama.com) - Local LLM inference
- [Terraform MCP Server](https://github.com/hashicorp/terraform-mcp-server) - Access to Terraform Registry
- [Model Context Protocol](https://modelcontextprotocol.io) - Standardized AI-tool communication
