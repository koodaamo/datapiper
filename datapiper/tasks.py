"Predefined tasks"

from .exceptions import PipelineTaskException
from .util import coroutine


@coroutine
def beginning(successor, meta=None):
   "pipeline start task"
   meta = meta or {}
   while True:
      data = yield
      successor.send((meta, data))


@coroutine
def task(operator, successor, meta=None):
   "regular pipeline worker task"
   meta = meta or {}
   while True:
      previous, data = yield
      meta["previous"] = previous
      print("running operator %s" % operator.__name__)
      try:
         result = operator(meta, data)
      except Exception as exc:
         raise PipelineTaskException("task %s failed: %s" % (operator.__name__, exc))
      else:
         del meta["previous"]
         successor.send((meta, result))


@coroutine
def ending(sinkmeta, sinkcallable=None):
   "pipeline end task"

   def meta_sink(meta, data):
      "a sink that just writes result to the pipeline meta"
      sinkmeta["result"] = {"meta": meta, "data": data}

   def callable_sink(meta, data):
      "a sink that also writes the result to a given callable"
      sinkmeta["result"] = {"meta": meta, "data": data}
      sinkcallable(data)

   sink = callable_sink if sinkcallable else meta_sink

   while True:
      finalmeta, finaldata = yield
      try:
         sink(finalmeta, finaldata)
      except Exception as exc:
         raise PipelineTaskException("sink callable failed: %s" % exc)
