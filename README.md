# Terraform Best Practices Analyzer

🔍 **AI-powered Terraform module analyzer** that provides actionable recommendations for improving security, performance, compliance, and cost optimization.

## ✨ Overview

Multi-agent system that analyzes your Terraform code and suggests improvements based on official Terraform Registry documentation and AWS best practices.

**Workflow:**
```
Terraform Code → Identify Services → Fetch Best Practices → Generate Recommendations
```

## ⚠️ Prerequisites (REQUIRED)

### 1. Docker (MUST BE RUNNING)
```bash
# Start Docker Desktop or Docker daemon
# Verify it's running:
docker ps

# Pull the Terraform MCP Server image:
docker pull hashicorp/terraform-mcp-server
```

### 2. Ollama (REQUIRED for local models)
```bash
# Install Ollama from: https://ollama.com

# Start Ollama service (must be running):
ollama serve

# Pull a model (7B+ recommended):
ollama pull llama3.2

# Verify Ollama is running:
ollama list
```

### 3. Python Dependencies
```bash
pip install -r requirements.txt
```

**⚠️ IMPORTANT:** Both Docker and Ollama **MUST be running** before executing the tool, otherwise it will fail.

## 🚀 Quick Start

**Before running, ensure:**
- ✅ Docker is running (`docker ps` works)
- ✅ Ollama is running (`ollama list` works)

**Run analysis:**
```bash
python main.py <terraform_module_directory>

# Example:
python main.py ./s3
```

**Output:** Analysis is saved to `terraform_analysis_<module>_<timestamp>.txt`

## 📊 Output

The tool generates a report with:

- **Current Implementation** - What you already have
- **Missing Best Practices** - What's missing (Security, Performance, Compliance, Cost)
- **Recommendations** - Specific Terraform resources to add with code examples
- **Priority Levels** - HIGH / MEDIUM / LOW for each recommendation


## 🏗️ Architecture

**Multi-agent system** with OOP design:

```
TerraformAnalyzer
    ├─→ ServiceAnalyzerAgent (Ollama) - Identifies AWS services
    ├─→ ResourcesFetcherAgent (Anthropic + MCP) - Queries Terraform Registry
    └─→ BestPracticesAdvisorAgent (Ollama) - Generates recommendations
```

**Key Features:**
- OOP design with base classes (`BaseAgent`, `OllamaAgent`, `AnthropicAgent`)
- PEP8 compliant
- Extensible and testable
- Proper separation of concerns

## 📋 System Requirements

**Essential:**
- Python 3.10+
- **Docker running** (verify with `docker ps`)
- **Ollama running** (verify with `ollama list`)

**Recommended Models:**
- `llama3.2` (7B) - Fast, good quality ✅ **Recommended**
- `llama3.1:8b` (8B) - Fast, good quality
- `mixtral:8x7b` (47B) - Best quality, slower

⚠️ **Note**: 3B models NOT recommended.

## 🔧 Configuration

**Change models** in `agents/config.py`:
```python
OLLAMA_MODEL_ID = "llama3.2"  # Change to your preferred model
```

**Programmatic usage:**
```python
from main import TerraformAnalyzer, MCPClientManager

with MCPClientManager() as mcp:
    analyzer = TerraformAnalyzer(mcp.list_tools())
    result = analyzer.analyze_module("./my-module")
```

**Custom agents:**
```python
from agents.base import OllamaAgent

class MyAgent(OllamaAgent):
    def analyze(self, data: str) -> str:
        return self.execute(f"Analyze: {data}")
```

## 📁 Project Structure

```
tf-bp-checker/
├── main.py              # Main orchestrator
├── agents/              # Multi-agent system
│   ├── base.py         # Base classes
│   ├── config.py       # Configuration
│   └── *_agent.py      # Specialized agents
├── requirements.txt     # Dependencies
└── s3/                 # Example module
```


## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Docker connection error** | Ensure Docker is running: `docker ps` |
| **Ollama connection error** | Start Ollama: `ollama serve` |
| **No Terraform files found** | Check directory path and `.tf` files exist |
| **Slow performance** | Use smaller model (llama3.2 instead of mixtral) |
| **Generic recommendations** | Use 7B+ model, not 3B |

**Most common issue:** Docker or Ollama not running. Always check both are active before running the tool.

## 📚 Resources

- [Terraform Registry](https://registry.terraform.io)
- [Ollama](https://ollama.com)
- [Strands Agents](https://strandsagents.com)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

**Built with:** Strands Agents • Ollama • Terraform MCP Server • Model Context Protocol
