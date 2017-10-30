"""The data piper implementation"""

import logging
from .exceptions import PipelineException
from .tasks import beginning, task, ending


logging.basicConfig()


def piper(ops, source=None, sink=None):
   "task runner posing as a generator (pull) or a coroutine (push)"

   # pull mode; operate as a generator
   if source and not sink:

      # construct the coroutine pipeline, last task first
      meta = {}
      end = ending(meta)
      tasks = [end]
      successor = end
      for taskop in ops[::-1]:
         tsk = task(taskop, successor)
         tasks.insert(0, tsk)
         successor = tsk

      # run the generator
      def generate(first):
         for data in source:
            # push each record into the pipeline
            first.send((meta, data))
            yield meta["result"]["data"]

      return generate(tasks[0])

   # push mode; operate as a coroutine
   elif sink and not source:
      meta = {}
      end = ending(meta, sinkcallable=sink)
      successor = end
      tasks = [end]
      for taskop in ops[::-1]:
         tsk = task(taskop, successor)
         tasks.insert(0, tsk)
         successor = tsk
      begin = beginning(tasks[0], meta)
      tasks.insert(0, begin)
      return begin

   else:
      raise PipelineException("invalid opertion mode")
