# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from typing import List, Tuple, Dict, Optional
from croniter import datetime_to_timestamp
from .job import Job

logger = logging.getLogger("cron-schedule")


class JobStore:

    def __init__(self):
        self.jobs: List[Tuple[Job, float]] = []
        self.jobs_index: Dict[str, Tuple[Job, float]] = {}

    def lookup_job(self, job_id: str) -> Optional[Job]:
        return self.jobs_index.get(job_id, (None, None))[0]

    def get_due_jobs(self, now: Optional[datetime] = None) -> List[Job]:
        now = now or datetime.now()
        now_timestamp = datetime_to_timestamp(now)
        pending = []
        for job, timestamp in self.jobs:
            if timestamp is None or timestamp > now_timestamp:
                break
            pending.append(job)

        return pending

    def add_job(self, job: Job):
        if job.job_id in self.jobs_index:
            raise Exception("Job already exists")
        logger.debug("Adding job %s", job)
        timestamp = datetime_to_timestamp(job.next_run_time)
        index = self._get_job_index(timestamp, job.job_id)
        self.jobs.insert(index, (job, timestamp))
        self.jobs_index[job.job_id] = (job, timestamp)

    def update_job(self, job: Job):
        old_job, old_timestamp = self.jobs_index.get(job.job_id, (None, None))
        if old_job is None:
            raise Exception("Job not found")
        old_index = self._get_job_index(old_timestamp, old_job.job_id)
        new_timestamp = datetime_to_timestamp(job.next_run_time)
        if old_timestamp == new_timestamp:
            self.jobs[old_index] = (job, new_timestamp)
        else:
            del self.jobs[old_index]
            new_index = self._get_job_index(new_timestamp, job.job_id)
            self.jobs.insert(new_index, (job, new_timestamp))

        self.jobs_index[job.job_id] = (job, new_timestamp)

    def remove_job(self, job_id: str):
        old_job, old_timestamp = self.jobs_index.get(job_id, (None, None))
        if old_job is None:
            raise Exception("Job not found")
        logger.debug("Removing job %s", old_job)
        index = self._get_job_index(old_timestamp, job_id)
        del self.jobs[index]
        del self.jobs_index[old_job.job_id]

    def remove_all_jobs(self):
        self.jobs = []
        self.jobs_index = {}

    def _get_job_index(self, timestamp: int, job_id: str):
        """
        二分查找
        :type timestamp: int
        :type job_id: str

        """
        lo, hi = 0, len(self.jobs)
        timestamp = float('inf') if timestamp is None else timestamp
        while lo < hi:
            mid = (lo + hi) // 2
            mid_job, mid_timestamp = self.jobs[mid]
            mid_timestamp = float('inf') if mid_timestamp is None else mid_timestamp
            if mid_timestamp > timestamp:
                hi = mid
            elif mid_timestamp < timestamp:
                lo = mid + 1
            elif mid_job.job_id > job_id:
                hi = mid
            elif mid_job.job_id < job_id:
                lo = mid + 1
            else:
                return mid

        return lo
