from abc import ABC, abstractmethod
import logging
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{agent_id}")
        
    @abstractmethod
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming data and return a response"""
        pass
    
    @abstractmethod
    def update_state(self, state_data: Dict[str, Any]) -> None:
        """Update agent's internal state"""
        pass