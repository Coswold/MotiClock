import datetime


def alarm_clock (hour, minute, dn):
    a_sec = (hour * 60 * 60) + (minute * 60)
    current_time = datetime.datetime.now()
    c_sec = (int(current_time.hour) * 60 * 60) + (int(current_time.minute) * 60)

    t_sec = a_sec - c_sec

    return t_sec
