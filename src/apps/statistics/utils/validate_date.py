from django.utils.timezone import now

from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

from apps.base.exceptions.exception_error import CustomExceptionError


def str_to_date(str_date: str):
    if not str_date:
        raise CustomExceptionError(
            code=400,
            detail="Date is required and must be in DD.MM.YYYY format."
    )
    try:
        date = datetime.strptime(str_date, "%d.%m.%Y").date()
    except ValueError:
        raise CustomExceptionError(
            code=400, detail="Invalid date format. Expected format is DD.MM.YYYY."
        )
    
    return date


def iterate_months(from_date: date, to_date: date):
    year = from_date.year
    month = from_date.month

    while (year < to_date.year) or (year == to_date.year and month <= to_date.month):
        yield date(year, month, 1)
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1


def validate_from_and_date_to_date(request):
    from_date_str = request.query_params.get("from_date")
    to_date_str = request.query_params.get("to_date")

    current_date = date(now().year, now().month, now().day)
    from_date = datetime.combine(current_date - relativedelta(months=11), time.min)
    to_date = datetime.combine(current_date, time.max)

    if from_date_str and to_date_str:
        from_date = str_to_date(str_date=from_date_str)
        to_date = str_to_date(str_date=to_date_str)

    if from_date >= to_date:
        raise CustomExceptionError(
            code=400, detail="The 'from_date' cannot be later than the 'to_date'."
        )

    twelve_month_later = from_date + relativedelta(months=12)
    if date(twelve_month_later.year, twelve_month_later.month, 1) <= date(to_date.year, to_date.month, 1):
        raise CustomExceptionError(
            code=400, detail="The date range cannot exceed 12 months."
        )
    
    return from_date, to_date