import datetime


# today = datetime.date.today()
# tomorrow = today + datetime.timedelta(days=1)

# print(tomorrow.strftime('%d.%m'))
# print(
#     (datetime.datetime.utcnow() + datetime.timedelta(hours=3)
# ).strftime('%H.%M'))


def check_date_for_schedule(schedule_time: datetime.datetime) -> bool:
    """
    функция для провреки даты в расписании
    """
    pass
    # if ((
    #     datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    # ).strftime('%H.%M') == schedule_time.strftime('%H.%M')):
    #     pass
