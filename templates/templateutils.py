import datetime

def since(otherdate):
    total_seconds = (datetime.datetime.now() - otherdate).total_seconds()
    days, seconds = divmod(total_seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    return "%dd %dh %dmi %ds" % (days, hours, minutes, seconds)
