# -*- coding: utf-8 -*-
from datetime import datetime
import time

from schedule import schedule


def do_some_job():
    print('do_some_job...', datetime.now())


schedule.add_job(do_some_job, "* * * * * 15,25")

while True:
    schedule.run_pending()
    time.sleep(1)
