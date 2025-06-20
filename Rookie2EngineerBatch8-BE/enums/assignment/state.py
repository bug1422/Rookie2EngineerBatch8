from enum import Enum

class AssignmentState(str, Enum):
    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    WAITING_FOR_ACCEPTANCE = "Waiting for acceptance"
    RETURNED = "Returned"
