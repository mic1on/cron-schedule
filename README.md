# cron-schedule

<a href="https://pypi.org/project/cron-schedule" target="_blank">
    <img src="https://img.shields.io/pypi/v/cron-schedule.svg" alt="Package version">
</a>

<a href="https://pypi.org/project/cron-schedule" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/cron-schedule.svg" alt="Supported Python versions">
</a>

## Installation

```bash
pip install cron-schedule 
```

## Usage

```python
from datetime import datetime
import time

from schedule import schedule


def do_some_job():
    print('do_some_job...', datetime.now())


schedule.add_job(do_some_job, "* * * * * 15,25")

while True:
    schedule.run_pending()
    time.sleep(1)
```

```text
do_some_job... 2022-09-23 15:35:15.152107
do_some_job... 2022-09-23 15:35:25.193932
```

#### thanks

- [croniter](https://github.com/kiorky/croniter)