import datetime
from dataclasses import dataclass


@dataclass
class Report:
    """Class for saving report info."""
    user_id: str
    is_realtime: bool
    timestamp: str
    location: (float, float)
    description: str

    def __init__(self, user_id: str, is_realtime: bool, timestamp: datetime, location: (float, float),
                 description: str):
        self.user_id = user_id
        self.is_realtime = is_realtime
        self.timestamp = timestamp.isoformat()
        self.location = location
        self.description = description
