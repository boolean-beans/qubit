from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    """config class for Qubit"""

    managers: List[int] = field(default_factory=list)
    staff_role: int = -1
    cooldown_rate: int = 5

    def __post__init__(self):
        # TODO: initialze config from database
        pass