import datetime


def get_year(request):
    year = datetime.datetime.now().year
    return {"year": year}