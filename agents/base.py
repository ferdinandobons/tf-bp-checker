"""
Base classes for Terraform Best Practices Analyzer agents.

This module provides abstract base classes and interfaces for all
specialized agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from strands import Agent
from strands.models.ollama import OllamaModel


class BaseAgent(ABC):
    """
    Abstract base class for all analyzer agents.
    
    All specialized agents should inherit from this class and implement
    the analyze method.
    
    Attributes:
        system_prompt: The system prompt for the agent
        model: Optional model instance
        tools: List of tools available to the agent
    """
    
    def __init__(
        self,
        system_prompt: str,
        model: Optional[Any] = None,
        tools: Optional[List] = None
    ):
        """
        Initialize the base agent.
        
        Args:
            system_prompt: The system prompt for the agent
            model: Optional model instance (defaults to None for Anthropic)
            tools: Optional list of tools available to the agent
            
        Raises:
            ValueError: If system_prompt is empty or None
        """
        if not system_prompt or not system_prompt.strip():
            raise ValueError("system_prompt cannot be empty")
        
        self.system_prompt = system_prompt
        self.model = model
        self.tools = tools or []
        self._agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """
        Create the underlying Strands agent instance.
        
        Returns:
            Configured Agent instance
        """
        agent_config: Dict[str, Any] = {
            'system_prompt': self.system_prompt,
        }
        
        if self.model is not None:
            agent_config['model'] = self.model
        
        if self.tools:
            agent_config['tools'] = self.tools
        
        return Agent(**agent_config)
    
    @abstractmethod
    def analyze(self, *args: Any, **kwargs: Any) -> str:
        """
        Perform the agent's analysis task.
        
        This method must be implemented by all subclasses to define
        their specific analysis logic.
        
        Args:
            *args: Positional arguments specific to the agent's task
            **kwargs: Keyword arguments specific to the agent's task
        
        Returns:
            Analysis results as a string
            
        Raises:
            NotImplementedError: If subclass doesn't implement this method
            
        Example:
            >>> class MyAgent(BaseAgent):
            ...     def analyze(self, data: str) -> str:
            ...         return self.execute(f"Analyze: {data}")
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement analyze() method"
        )
    
    def execute(self, prompt: str) -> str:
        """
        Execute the agent with the given prompt.
        
        Args:
            prompt: The prompt to execute
            
        Returns:
            Agent response as string
            
        Raises:
            ValueError: If prompt is empty
        """
        if not prompt or not prompt.strip():
            raise ValueError("prompt cannot be empty")
        
        try:
            response = self._agent(prompt)
            return str(response)
        except Exception as e:
            error_msg = f"Error executing agent: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def __repr__(self) -> str:
        """
        Return string representation of the agent.
        
        Returns:
            String representation showing class name and model info
        """
        model_info = (
            f"model={self.model.__class__.__name__}"
            if self.model else "model=Anthropic"
        )
        tools_info = f"tools={len(self.tools)}"
        return f"{self.__class__.__name__}({model_info}, {tools_info})"
    
    def __str__(self) -> str:
        """
        Return user-friendly string representation.
        
        Returns:
            Readable string describing the agent
        """
        return (
            f"{self.__class__.__name__} with "
            f"{len(self.tools)} tool(s)"
        )


class OllamaAgent(BaseAgent):
    """
    Base class for agents using Ollama models.
    
    Provides common configuration for Ollama-based agents with
    sensible defaults for local inference.
    
    Attributes:
        host: Ollama server host URL
        model_id: Model identifier
        max_tokens: Maximum tokens for generation
        temperature: Sampling temperature (0.0 to 1.0)
        keep_alive: Keep-alive duration for model
    """
    
    def __init__(
        self,
        system_prompt: str,
        host: str = "http://localhost:11434",
        model_id: str = "llama3.2",
        max_tokens: int = 20000,
        temperature: float = 0.1,
        keep_alive: str = "10m",
        tools: Optional[List] = None
    ):
        """
        Initialize Ollama agent with model configuration.
        
        Args:
            system_prompt: The system prompt for the agent
            host: Ollama server host URL (default: http://localhost:11434)
            model_id: Model identifier (default: llama3.2)
            max_tokens: Maximum tokens for generation (default: 20000)
            temperature: Sampling temperature 0.0-1.0 (default: 0.1)
            keep_alive: Keep-alive duration for model (default: 10m)
            tools: Optional list of tools
            
        Raises:
            ValueError: If temperature is not between 0.0 and 1.0
            ValueError: If max_tokens is not positive
        """
        if not 0.0 <= temperature <= 1.0:
            raise ValueError(
                f"temperature must be between 0.0 and 1.0, got {temperature}"
            )
        if max_tokens <= 0:
            raise ValueError(
                f"max_tokens must be positive, got {max_tokens}"
            )
        self.host = host
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.keep_alive = keep_alive
        
        # Create Ollama model instance
        model = OllamaModel(
            host=self.host,
            model_id=self.model_id,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            keep_alive=self.keep_alive,
        )
        
        super().__init__(
            system_prompt=system_prompt,
            model=model,
            tools=tools
        )


class AnthropicAgent(BaseAgent):
    """
    Base class for agents using Anthropic models.
    
    Uses the default Anthropic model configuration from Strands.
    This is typically used for agents that need access to MCP tools
    or require Claude's advanced capabilities.
    """
    
    def __init__(
        self,
        system_prompt: str,
        tools: Optional[List] = None
    ):
        """
        Initialize Anthropic agent.
        
        Args:
            system_prompt: The system prompt for the agent
            tools: Optional list of tools (e.g., MCP tools)
        """
        super().__init__(
            system_prompt=system_prompt,
            model=None,  # None uses default Anthropic model
            tools=tools
        )

