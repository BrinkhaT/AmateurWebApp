from datetime import datetime, timedelta
from random import randint

def calc_next_start_time(seconds, variation):
    now = datetime.utcnow
    timediff =  randint(round(seconds * (1-variation)), round(seconds * (1+variation)))
    nextStart = datetime.now() + timedelta(seconds=timediff)

    return nextStart