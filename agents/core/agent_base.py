from abc import ABC, abstractmethod

class AgentBase(ABC):
    """Abstract base class for all agents"""

    def __init__(self, config, comm, logger):
        self.config = config
        self.comm = comm
        self.logger = logger

    @abstractmethod
    def run(self):
        """Main entry point for agent execution"""
        pass

    @abstractmethod
    def process_message(self, topic, message):
        """Process incoming messages"""
        pass