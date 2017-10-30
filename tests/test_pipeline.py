from datapiper.piper import piper


def test_simple():
   "first simple test"

   def op1(meta, data):
      "define first task operation"
      return (data[0], data[1], 9)

   def op2(meta, data):
      "define second task operation"
      data = list(data)
      data.append(sum(data))
      return data

   # list of task operations
   ops = (op1, op2)

   # data source to be processed
   source = [(1,2),(2,3),(3,4)]

   # instantiate the jolly piper
   p = piper(ops, source)

   # check that the outcome is as it should
   result = [r for r in p]
   assert result == [[1, 2, 9, 12], [2,3,9, 14], [3, 4, 9, 16]]
