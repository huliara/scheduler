import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class IEntity(ABC):
    id: uuid.UUID
    @classmethod
    @abstractmethod
    def from_model(cls, data) -> 'IEntity':
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
