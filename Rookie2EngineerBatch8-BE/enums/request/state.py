from enum import Enum

class RequestState(str, Enum):
    COMPLETED = "Completed"
    WAITING_FOR_RETURNING = "Waiting for returning"
