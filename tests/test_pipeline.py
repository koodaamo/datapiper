from datapiper.piper import Piper
from setup import ops, op3, datasource, datasink, expected


def test_simple_generator():
   "simple generator test"

   # instantiate the jolly piper
   p = Piper(ops, source=datasource)

   # check that the outcome is as it should
   result = [r for r in p]
   assert result == expected


def test_simple_coroutine():
   "simple coroutine test"

   # instantiate the jolly piper
   p = Piper(ops, sink=datasink)

   # send the data and check the result
   results = []
   for d in datasource:
      p.send(d)
      results.append(p.context["result"])

   # check that the outcome is as it should
   assert results == expected


def test_pipe_doc():
   "simple documentation test"

   p = Piper(ops, sink=datasink)
   assert str(p) == "op1 > op2 > sink"


def test_context_setting():
   "simple operation-performed context mutation test"

   ops = (op3,)
   p = Piper(ops, sink=datasink)
   p.send("test")
   assert p.context["result"] == "test"
   assert p.context["flag"] == True