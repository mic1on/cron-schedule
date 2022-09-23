# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from typing import Callable, Optional

from .job import Job, RemoveJob
from .store import JobStore

logger = logging.getLogger("cron-schedule")


class JobLookupError(KeyError):
    def __init__(self, job_id):
        super(JobLookupError, self).__init__(f'job id of `{job_id}` was not found')


class Schedule:
    def __init__(self):
        self.job_store = JobStore()

    def add_job(self, job_func: Callable, cron: str, job_id=None, *args, **kwargs) -> Job:
        job_kwargs = {
            'job_id': job_id,
            'cron': cron,
            'args': args,
            'kwargs': kwargs
        }
        job = Job(self, job_func, **job_kwargs)

        now = datetime.now()
        job.next_run_time = job.trigger.get_next_fire_time(None, now)
        self.job_store.add_job(job)
        return job

    def pause_job(self, job_id: str) -> Job:
        logger.debug(f"pause job {job_id}")
        return self.modify_job(job_id, next_run_time=None)

    def resume_job(self, job_id: str) -> Optional[Job]:
        logger.debug(f"resume job {job_id}")
        job = self._lookup_job(job_id)
        now = datetime.now()
        next_run_time = job.trigger.get_next_fire_time(None, now)
        if next_run_time:
            return self.modify_job(job_id, next_run_time=next_run_time)
        else:
            self.job_store.remove_job(job_id)

    def _run_job(self, job: Job):
        ret = job.run()
        if isinstance(ret, RemoveJob) or ret is RemoveJob:
            self.job_store.remove_job(job.job_id)
        else:
            self.job_store.update_job(job)

    def modify_job(self, job_id: str, **changes) -> Job:
        job = self._lookup_job(job_id)
        job.modify(**changes)
        self.job_store.update_job(job)
        return job

    def _lookup_job(self, job_id: str) -> Job:
        job = self.job_store.lookup_job(job_id)
        if job is not None:
            return job
        raise JobLookupError(job_id)

    def run_pending(self):
        due_jobs = self.job_store.get_due_jobs()

        for job in due_jobs:
            self._run_job(job)
