from enum import Enum


class Id(Enum):
    USER_ID_VALID = 1
    USER_ID_NOT_EXIST = 9999


class Name(Enum):
    """Can be used for first name and last name"""

    NAME_VALID = "Test"
    NAME_EXCEED_MAX_LENGTH_128 = "a" * 129
    NAME_EMPTY = ""
    NAME_SPECIAL_CHARACTER = "Test@123"
    NAME_ONLY_SPACE = " "
    NAME_ONLY_NUMBER = 123456
    NAME_NUMBER_STRING = "123456"
    NAME_NULL = None
    NAME_MAX_LENGTH = "a" * 128
    NAME_MIN_LENGTH = "a"


class DateOfBirth(Enum):
    DATE_OF_BIRTH_VALID = "1990-01-01"
    DATE_OF_BIRTH_FUTURE = "2099-01-01"
    DATE_OF_BIRTH_UNDER_18 = "2005-01-01"
    DATE_OF_BIRTH_NULL = None


class JoinDate(Enum):
    JOIN_DATE_VALID = "2023-01-01"
    JOIN_DATE_FUTURE = "2099-01-01"
    JOIN_DATE_BEFORE_DOB = "1989-01-01"  # Before DATE_OF_BIRTH_VALID
    JOIN_DATE_NULL = None


class Gender(Enum):
    GENDER_VALID_MALE = "male"
    GENDER_VALID_FEMALE = "female"
    GENDER_INVALID = "invalid"
    GENDER_NULL = None


class Type(Enum):
    TYPE_VALID_STAFF = "staff"
    TYPE_VALID_ADMIN = "admin"
    TYPE_INVALID = "invalid"
    TYPE_NULL = None


class Location(Enum):
    LOCATION_VALID_HANOI = "Hanoi"
    LOCATION_VALID_HCM = "Ho Chi Minh"
    LOCATION_VALID_DANANG = "Danang"
    LOCATION_INVALID = "invalid"
    LOCATION_NULL = None


class Status(Enum):
    STATUS_VALID_ACTIVE = "active"
    STATUS_VALID_DISABLED = "disabled"
    STATUS_INVALID = "invalid"
    STATUS_NULL = None


class IsFirstLogin(Enum):
    IS_FIRST_LOGIN_VALID_TRUE = "true"
    IS_FIRST_LOGIN_VALID_FALSE = "false"
    IS_FIRST_LOGIN_INVALID = "invalid"
    IS_FIRST_LOGIN_NULL = None


class InstalledDate(Enum):
    INSTALLED_DATE_VALID = "2023-01-01"
    INSTALLED_DATE_FUTURE = "2099-01-01"
    INSTALLED_DATE_NULL = None
    INSTALLED_DATE_BEFORE_CREATED = "2022-12-31"  # Before CREATED_AT
    INSTALLED_DATE_AFTER_CREATED = "2023-01-02"  # After CREATED_AT