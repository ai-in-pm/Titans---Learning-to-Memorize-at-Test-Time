from abc import ABC, abstractmethod
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

class TitansAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        load_dotenv()
        
    @abstractmethod
    async def demonstrate(self) -> Dict[str, Any]:
        """Execute the agent's main demonstration"""
        pass
        
    @abstractmethod
    async def interact(self, user_input: str) -> str:
        """Handle user interactions"""
        pass
        
    @abstractmethod
    async def collaborate(self, other_agent_data: Dict[str, Any]) -> str:
        """Collaborate with other agents"""
        pass
        
    @abstractmethod
    def get_metrics(self) -> Dict[str, float]:
        """Return performance metrics"""
        pass
        
    @abstractmethod
    def visualize(self) -> Dict[str, Any]:
        """Generate visualizations"""
        pass
