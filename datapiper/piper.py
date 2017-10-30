"""The data piper implementation"""

import logging
from .exceptions import PipelineException
from .tasks import beginning, task, ending


logging.basicConfig()


def piper(ops, source=None, sink=None):
   "task runner posing as a generator (pull) or a coroutine (push)"

   # pipeline global metadata
   meta = {}

   # construct the coroutine pipeline, last task first
   end = ending(meta, sinkcallable=sink)
   tasks = [end]

   successor = end

   for taskop in ops[::-1]:
      tsk = task(taskop, successor)
      tasks.insert(0, tsk)
      successor = tsk

   # pull mode; provide a generator
   if source and not sink:

      def generate(first):
         for data in source:
            # push each record into the pipeline
            first.send((meta, data))
            # and yield the result
            yield meta["result"]["data"]

      return generate(tasks[0])

   # push mode; provide a coroutine
   elif sink and not source:
      begin = beginning(tasks[0], meta)
      tasks.insert(0, begin)
      return begin # ie. the first task of the pipeline

   else:
      raise PipelineException("invalid opertion mode")
