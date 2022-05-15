from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    """config class for Qubit"""

    managers: List[int] = field(default_factory=list)
    staff_role: int = -1
    media_perms_role: int = -1
    mute_role: int = -1
    skid_role: int = -1
    logging_channel: int = -1

    def __post__init__(self):
        # TODO: initialize config from database
        pass
