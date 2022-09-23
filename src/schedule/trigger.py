# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from typing import Optional

from croniter import croniter


class CrontabTrigger:

    def __init__(self, cron_expr: str):
        """
        :param str cron_expr: cron表达式
        """
        self.cron_expr = cron_expr

    def _calc_next_time(self, start_date: Optional[datetime] = None):
        iter = croniter(self.cron_expr, start_date)  # noqa
        return iter.get_next(datetime)

    def get_next_fire_time(self,
                           previous_fire_time: Optional[datetime] = None,
                           now: Optional[datetime] = None) -> datetime:
        now = now or datetime.now()
        if previous_fire_time:
            start_date = min(now, previous_fire_time + timedelta(microseconds=1))
            if start_date == previous_fire_time:
                start_date += timedelta(microseconds=1)
        else:
            start_date = now

        next_date = start_date
        next_date = self._calc_next_time(next_date)

        return next_date
