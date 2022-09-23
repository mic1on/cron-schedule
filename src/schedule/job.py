# -*- coding: utf-8 -*-
import functools
import logging
from typing import Callable
from uuid import uuid4

from .trigger import CrontabTrigger

logger = logging.getLogger("cron-schedule")


class RemoveJob:
    pass


class Job:

    def __init__(self, scheduler, job_func: Callable, job_id=None, **kwargs):
        self.scheduler = scheduler
        self.job_id = job_id or uuid4().hex
        self.next_run_time = None
        self.trigger = CrontabTrigger(kwargs.get('cron'))

        self.job_func = functools.partial(job_func,
                                          *kwargs.get('args'),
                                          **kwargs.get('kwargs'))
        functools.update_wrapper(self.job_func, job_func)

    def _configuration(self):
        pass

    def modify(self, next_run_time):
        self.next_run_time = next_run_time

    def pause(self):
        self.scheduler.pause_job(self.job_id)
        return self

    def resume(self):
        self.scheduler.resume_job(self.job_id)
        return self

    def run(self):
        logger.debug(f"Running job {self.job_id}")
        ret = self.job_func()

        job_next_run_time = self.trigger.get_next_fire_time(self.next_run_time)
        if job_next_run_time:
            self.modify(next_run_time=job_next_run_time)
            return ret
        else:
            return RemoveJob

    def __repr__(self):
        return f'<Job (id={self.job_id} name={self.job_func.__name__})>'
