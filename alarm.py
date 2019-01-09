import datetime

def alarm_clock (hour, minute, dn):
    if dn == 1:
        hour += 12
    alarm_time = datetime.time(hour, minute).strftime("%I:%M %p")
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    print(alarm_time)
    print(current_time)

    while alarm_time != current_time:
        current_time = datetime.datetime.now().strftime("%I:%M %p")

    return True
