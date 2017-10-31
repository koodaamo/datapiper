def op1(meta, data):
   "define first task operation"
   return (data[0], data[1], 9)

def op2(meta, data):
   "define second task operation"
   data = list(data)
   data.append(sum(data))
   return data

ops = (op1, op2)

# data source to be processed
datasource = [(1,2),(2,3),(3,4)]


# data sink receiving the result
result = []
def datasink(data):
   result.append(data)


#expected pipeline output
expected = [[1, 2, 9, 12], [2,3,9, 14], [3, 4, 9, 16]]