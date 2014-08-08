import datetime


def current_date(request):
    return {'current_date': datetime.datetime.now()}
