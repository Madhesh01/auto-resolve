from pydantic import BaseModel
from enum import Enum 
from typing import Optional

class CaseStatus(str, Enum):
    pending = "Pending"
    in_progress = "In Progress"
    resolved = "Resolved"
    flagged = "Flagged"
    needs_info = "Needs Info"


class Ticket(BaseModel): 
    case_id: Optional[int] = None
    case_title: str
    case_owner: str
    case_description: str
    case_status: CaseStatus
    ai_resolution: Optional[str] = None

