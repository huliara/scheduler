import uuid
from dataclasses import dataclass
from typing import NewType

TaskId = NewType('TaskId', uuid.UUID)
