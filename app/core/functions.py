import datetime
from datetime import datetime as dtime
from django.utils import timezone
from zoneinfo import ZoneInfo


def hours_zone(date):
    date_time = dtime(
        date.year,
        date.month,
        date.day,
        date.hour,
        date.minute,
        date.second,
        date.microsecond,
        tzinfo=ZoneInfo('America/Chihuahua')
    )
    string_date = str(date_time)
    hours = int(string_date[-5:-3])
    minutes = int(string_date[-2:])
    more_or_less = string_date[-6]
    return [more_or_less, hours, minutes, date_time]


def read_orders_in_local_time(created):
    """
    Only DateTimeField:
    format="%d/%m/%Y %H:%M"
    """
    date_time = dtime(
        int(created[6:10]),
        int(created[3:5]),
        int(created[:2]),
        int(created[11:13]),
        int(created[14:]),
        tzinfo=ZoneInfo('America/Chihuahua')
    )
    string_date = str(date_time)
    hours = int(string_date[-5:-3])
    minutes = int(string_date[-2:])
    more_or_less = string_date[-6]
    if more_or_less == '-':
        date_converted = (date_time - datetime.timedelta(hours=hours,
                          minutes=minutes)).strftime('%d/%m/%Y %H:%M')
    elif more_or_less == '+':
        date_converted = (date_time + datetime.timedelta(hours=hours,
                          minutes=minutes)).strftime('%d/%m/%Y %H:%M')
    return str(date_converted)


def lastest_canceled_and_next_allowed(range_days, query):
    try:
        canceled_orders = query.filter(canceled=True)[0:3]
        before_days = timezone.now() - datetime.timedelta(days=range_days)
        before_no_hours = before_days.replace(hour=0, minute=0, second=0)
        acc = 0
        for canceled_order in canceled_orders:
            if canceled_order.creation_date > before_no_hours:
                acc += 1
        if acc >= 3:
            next_order_allowed = (
                canceled_orders[0].creation_date +
                datetime.timedelta(days=range_days)
            ).strftime('%d/%m/%Y %H:%M')
            return next_order_allowed
    except:
        pass


def query_date_major_or_minor():
    more_or_less = hours_zone(timezone.now())[0]
    hours = hours_zone(timezone.now())[1]
    minutes = hours_zone(timezone.now())[2]
    today = timezone.now()
    date_now = dtime(
            today.year,
            today.month,
            today.day,
            today.hour,
            today.minute,
            today.second,
            today.microsecond
        )
    if more_or_less == '-':
        date_now = date_now - datetime.timedelta(hours=hours, minutes=minutes)
        date_now = dtime(
            date_now.year,
            date_now.month,
            date_now.day
        )
        lower_date = date_now + datetime.timedelta(
            hours=hours,
            minutes=minutes
        )
        higher_date = date_now + datetime.timedelta(
            days=1,
            hours=hours,
            minutes=minutes
        )
    if more_or_less == '+':
        date_now = date_now + datetime.timedelta(hours=hours, minutes=minutes)
        date_now = dtime(
            date_now.year,
            date_now.month,
            date_now.day
        )
        lower_date = date_now - datetime.timedelta(
            hours=hours,
            minutes=minutes
        )
        higher_date = date_now + datetime.timedelta(
            days=1,
            hours=-hours,
            minutes=-minutes
        )
    return [lower_date, higher_date]
