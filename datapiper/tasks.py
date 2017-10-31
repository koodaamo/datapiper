"Predefined tasks"

from .exceptions import PipelineTaskException
from .util import coroutine


@coroutine
def beginning(successor, context=None):
   "pipeline start task"
   context = context or {}
   while True:
      data = yield
      successor.send((context, data))


@coroutine
def task(operator, successor, context=None):
   "regular pipeline worker task"
   context = context or {}
   while True:
      previous, data = yield
      context["previous"] = previous
      try:
         result = operator(context, data)
      except Exception as exc:
         raise PipelineTaskException("task %s failed: %s" % (operator.__name__, exc))
      else:
         del context["previous"]
         successor.send((context, result))


@coroutine
def ending(sinkcontext, sinkcallable=None):
   "pipeline end task"

   def context_sink(context, data):
      "a sink that just writes result to the pipeline context"
      sinkcontext["result"] = {"context": context, "data": data}

   def callable_sink(context, data):
      "a sink that also writes the result to a given callable"
      sinkcontext["result"] = {"context": context, "data": data}
      sinkcallable(data)

   sink = callable_sink if sinkcallable else context_sink

   while True:
      finalcontext, finaldata = yield
      try:
         sink(finalcontext, finaldata)
      except Exception as exc:
         raise PipelineTaskException("sink callable failed: %s" % exc)
