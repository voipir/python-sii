# -*- coding: utf-8 -*-
""" Protocol Helpers.
"""
import time


__all__ = [
    'with_retry'
]

RETRIES_MAX   = 5
RETRIES_SLEEP = 1


def with_retry(func, count=RETRIES_MAX, ival=RETRIES_SLEEP):
    retries = 0
    while retries < count:
        try:
            return func()
        except Exception as exc:
            code, msg = exc.args[0]

            if code == 503:
                retries += 1
                time.sleep(ival)
                continue
            else:
                raise
