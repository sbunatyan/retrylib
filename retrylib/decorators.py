#!/usr/bin/env python
# Copyright (c) 2014 Sergey Bunatyan <sergey.bunatyan@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import collections
import functools
import time
import types


class CatchStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def need_to_retry(self, exc):
        pass


class CatchFunctionStrategy(CatchStrategy):

    def __init__(self, to_retry):
        super(CatchFunctionStrategy, self).__init__()
        self._to_retry = to_retry

    def need_to_retry(self, exc):
        return self._to_retry(exc)


class CatchExceptionStrategy(CatchFunctionStrategy):

    def __init__(self, exceptions_to_retry):
        self._exceptions_to_retry = exceptions_to_retry
        retry_exceptions = self._to_tuple()
        super(CatchExceptionStrategy, self).__init__(
            lambda exc: isinstance(exc, retry_exceptions))

    def _to_tuple(self):
        if isinstance(self._exceptions_to_retry, collections.Iterable):
            retry_exceptions = tuple(self._exceptions_to_retry)
        else:
            retry_exceptions = (self._exceptions_to_retry,)
        return retry_exceptions


def retry(attempts_number, delay=0, step=0, retry_on=Exception, logger=None):
    """Reties function several times

    @param attempts_number: number of function calls (first call + retries)
    @param delay: delay before first retry
    @param step: increment value of timeout on each retry
    @param retry_on: exception that should be handled or function that checks
                     if retry should be executed (default: Exception)
    @param logger: logger to write warnings

    @return: the result of decorated function
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_logger = logger

            attempts = 1
            retry_delay = delay

            try:
                if isinstance(args[0], object):
                    current_logger = args[0].get_logger()
            except (AttributeError, IndexError):
                pass

            if isinstance(retry_on, (types.FunctionType,
                                     types.MethodType,)):
                catch_strategy = CatchFunctionStrategy(retry_on)
            else:
                catch_strategy = CatchExceptionStrategy(retry_on)

            while attempts <= attempts_number:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if catch_strategy.need_to_retry(e):
                        if attempts >= attempts_number:
                            raise
                        elif current_logger:
                            current_logger.warning(
                                "Retry: Call to %(fn)s failed due to "
                                "%(exc_class)s: %(exc)s, retry "
                                "attempt #%(retry_no)s/"
                                "%(retry_count)s after %(delay)ss",
                                dict(fn=func.__name__,
                                     exc=str(e),
                                     retry_no=attempts,
                                     exc_class=e.__class__.__name__,
                                     retry_count=attempts_number - 1,
                                     delay=retry_delay))
                        time.sleep(retry_delay)
                        attempts += 1
                        retry_delay += step
                    else:
                        raise
        return wrapper
    return decorator
