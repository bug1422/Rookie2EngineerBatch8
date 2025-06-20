from datetime import datetime

from enums.user.type import Type
from enums.user.gender import Gender
from enums.user.status import Status
from enums.shared.location import Location
from schemas.user import UserCreate, UserRead

def get_mock_user_create():
    return UserCreate(
        first_name="Test",
        last_name="User",
        date_of_birth=datetime(1990, 1, 1),
        join_date=datetime(2023, 1, 2),
        type=Type.ADMIN,
        gender=Gender.MALE,
        location=Location.HANOI,
    )
    
def get_mock_user_read():
    now = datetime.now()
    return UserRead(
        id=1,
        username="testu",
        staff_code="SD0001",
        status=Status.ACTIVE,
        first_name="Test",
        last_name="User",
        date_of_birth=datetime(1990, 1, 1),
        join_date=datetime(2023, 1, 2),
        type=Type.ADMIN,
        gender=Gender.MALE,
        location=Location.HANOI,
        is_first_login=True,
        created_at=now,
        updated_at=now
    )