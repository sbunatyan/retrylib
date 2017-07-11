Library to make code more robust
================================

Retry decorator parameters
--------------------------

retry(attempts_number, delay=0, step=0, max_delay=-1, retry_on=Exception, logger=None)

* attempts_number: number of function calls (first call + retries). If attempts_number < 0 then retry infinitely
* delay: delay before first retry
* step: increment value of timeout on each retry
* max_delay: maximum delay value (upper bound for delay)
* retry_on: exception that should be handled or function that checks
                     if retry should be executed (default: Exception)
* logger: logger to write warnings

returns the result of decorated function


Retry on specific exception
---------------------------

  from retrylib import retry

  @retry(attempts_number=3, retry_on=(MyException,))
  def function():
      raise MyException()


Use custom function
-------------------

  from retrylib import retry

  def is_my_exception(error):
      return isinstance(error, MyException)

  @retry(attempts_number=3, retry_on=is_my_exception)
  def function():
      raise MyException()


Retry on network errors
-----------------------

You can use following code to add retries for your custom network
function:

  import requests
  from retrylib.network import retry

  @retry()
  def function():
     response = requests.get('http://localhost:5002')
     response.raise_for_status()
     return response

  function()


Logging
=======

Global logger
-------------

You can pass specific logger to decorator:

  import logging
  import logging.config

  from retrylib.network import retry


  LOGGING = {
      'version': 1,
      'formatters': {
          'precise': {
              'datefmt': '%Y-%m-%d,%H:%M:%S',
              'format': '%(levelname)-7s %(asctime)15s '
                        '%(name)s:%(lineno)d %(message)s'
          }
      },
      'handlers': {
          'console': {
              'class': 'logging.StreamHandler',
              'formatter': 'precise',
              'stream': 'ext://sys.stderr'
          },
      },
      'root': {
          'level': 'INFO',
          'handlers': ['console']
      }
  }

  logging.config.dictConfig(LOGGING)

  LOGGER = logging.getLogger(__name__)

  @retry(logger=LOGGER)
  def function():
     response = requests.get('http://localhost:5002')
     response.raise_for_status()
     return response


Object-specific logger
----------------------


To use object-specific logger define method 'get_logger'

  from retrylib import retry


  class MyClass(object):
     def __init__(self):
         self._logger = logging.getLogger(__name__)

     def get_logger(self):
         return self._logger

     @retry()
     def my_method(self):
         pass

  obj = MyClass()
  obj.my_method()
  # obj._logger will be used
