=====================
Logging Configuration
=====================

Most components of Auraxium log their status via the :mod:`logging` module to help monitor their performance and troubleshoot potential issues.

The following snippet will, if placed before your application code, log all but the most spammy messages to your console:

.. code-block:: python3

   import logging

   logging.basicConfig(level=logging.INFO)

Alternatively, the following snippet is an example of a more comprehensive logging setup, only keeping warnings and errors in the console while still logging to disk at full resolution. This option is recommended for troubleshooting:

.. code-block:: python3

   import logging

   # Logging configuration
   fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
   fh = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w+')
   fh.setFormatter(fmt)
   sh = logging.StreamHandler()
   sh.setFormatter(fmt)
   sh.setLevel(logging.WARNING)

   log = logging.getLogger('auraxium')
   log.setLevel(logging.DEBUG)
   log.addHandler(fh)
   log.addHandler(sh)

Logger Hierarchy
================

The following loggers are available in Auraxium. You can subscribe to a single logger's messages using its qualified name, e.g. ``logging.getLogger('auraxium.ess')``.

`auraxium`:
   `auraxium.client`:
      API client performance monitoring and latency information
   `auraxium.ess`:
      Event stream performance and trigger dispatching
   `auraxium.ps2`:
      Object instantiation
   `auraxium.http`:
      HTTP session, requests and exponential backoff
   `auraxium.cache`:
      Cache misses and usage

For more information on log messages, filters and configuration option, please refer to the Python docs' `logging Cookbook`_.

.. _logging Cookbook: https://docs.python.org/3/howto/logging-cookbook.html
