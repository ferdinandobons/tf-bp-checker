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

### Multi-Agent System

The tool uses a **modular multi-agent architecture** with specialized agents coordinated by an orchestrator:

```
main.py (Orchestrator)
    ↓
    ├─→ agents/service_analyzer_agent.py (Agent 1)
    │   └─→ Identifies AWS services in code
    │
    ├─→ agents/resources_fetcher_agent.py (Agent 2)
    │   └─→ Queries Terraform Registry via MCP
    │
    └─→ agents/best_practices_advisor_agent.py (Agent 3)
        └─→ Generates actionable recommendations
```

### Agent Details

| Agent | File | Model | Purpose | Tools |
|-------|------|-------|---------|-------|
| **Service Analyzer** | `service_analyzer_agent.py` | Ollama (llama3.2) | Identifies AWS services in Terraform code | - |
| **Resources Fetcher** | `resources_fetcher_agent.py` | Anthropic (default) | Queries Terraform Registry for best practices | 34 MCP tools |
| **Best Practices Advisor** | `best_practices_advisor_agent.py` | Ollama (llama3.2) | Compares code with best practices and generates recommendations | - |

### Why This Design?

- **Modular architecture**: Each agent is a separate file with clear responsibilities
- **Ollama agents**: Fast, local processing for code analysis and recommendations
- **MCP agent**: Direct access to official Terraform Registry documentation
- **Separation of concerns**: Easy to maintain, test, and extend individual agents
- **Reusable components**: Agents can be imported and used independently

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

The tool uses Ollama for analysis agents. To change the model, edit the agent files:

**For Service Analyzer:**
```python
# In agents/service_analyzer_agent.py, line 4-10
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2",  # Change this
    max_tokens=20000,
    temperature=0.1,
    keep_alive="10m",
)
```

**For Best Practices Advisor:**
```python
# In agents/best_practices_advisor_agent.py, line 4-10
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2",  # Change this
    max_tokens=20000,
    temperature=0.1,
    keep_alive="10m",
)
```

### Using Default Anthropic Model

To use Anthropic's Claude instead of Ollama for analysis:

```python
# In agents/service_analyzer_agent.py or agents/best_practices_advisor_agent.py
# Comment out the model parameter in the Agent creation:
agent = Agent(
    # model=ollama_model,  # Comment this line
    system_prompt=SYSTEM_PROMPT,
)
```

### Extending the System

Thanks to the modular architecture, you can easily:

**Add new agents:**
```python
# Create agents/new_custom_agent.py
from strands import Agent, tool

@tool
def new_analysis_function(data: str) -> str:
    agent = Agent(system_prompt="...")
    return agent(data)
```

**Customize existing agents:**
Each agent file is self-contained and can be modified independently without affecting others.

## 📁 Project Structure

### Tool Structure

```
terraform-suggestions/
├── main.py                              # Orchestrator that coordinates all agents
├── agents/                              # Multi-agent system
│   ├── __init__.py                     # Package initialization
│   ├── service_analyzer_agent.py       # Agent 1: Identifies AWS services
│   ├── resources_fetcher_agent.py      # Agent 2: Queries Terraform Registry
│   └── best_practices_advisor_agent.py # Agent 3: Generates recommendations
├── requirements.txt                     # Python dependencies
├── README.md                            # Documentation
└── example_output.txt                   # Sample analysis output
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
