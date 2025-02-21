import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.database import Base


@dataclass
class IEntity(ABC):
    id: uuid.UUID
    @classmethod
    @abstractmethod
    def from_model(cls, data: Base) -> 'IEntity':
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
