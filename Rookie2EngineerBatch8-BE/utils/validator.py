from datetime import date
from dateutil.relativedelta import relativedelta

class Validator:
    @staticmethod
    def validate_age_at_least(date_of_birth: date, age: int) -> bool:
        min_date = date.today() - relativedelta(years=age)
        return date_of_birth <= min_date