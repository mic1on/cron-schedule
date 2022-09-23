# -*- coding: utf-8 -*-
from calendar import timegm


def datetime_to_timestamp(timeval):
    if timeval is not None:
        return timegm(timeval.timetuple()) + timeval.microsecond / 1000000
