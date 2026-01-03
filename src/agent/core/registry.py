from typing import List, Dict, Any, Callable
from langchain_core.tools import BaseTool

class ToolRegistry:
    """
    A simple registry to manage tools at runtime.
    This allows middleware to easily discover and wrap tools.
    """
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        self._tools[tool.name] = tool

    def get_tools(self) -> List[BaseTool]:
        return list(self._tools.values())

    def get_tool(self, name: str) -> BaseTool:
        return self._tools.get(name)

# Global registry instance
registry = ToolRegistry()
