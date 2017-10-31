===============================
Overview
===============================

Datapiper provides a flexible easy-to-use library for constructing and running
simple data batch processing pipelines.

Give Datapiper your list of data processing callables and it will construct a
runnable data pipeline for you.

If you instantiate the pipe with a (iterable) data source, you get a generator
that reads from a source and outputs processed data for you:

.. code-block::

   >>> operations = [lambda context, data: data+1]
   >>> datasource = [1,2,3]
   >>> p = Piper(operations, source=datasource)
   >>> print p
   pipe: source > <lambda>
   >>> [r for r in p]
   [2,3,4]

If you instead instantiate it with a (callable) data sink, you get a coroutine
that accepts data from a producer and delivers processed data to a sink:

.. code-block::

   >>> operations = [lambda context, data: data+1]
   >>> results = []
   >>> def datasink(data):
   ...    results.append(data)
   >>> p = Piper(operations, sink=datasink)
   >>> print p
   pipe: <lambda> > sink
   >>> for v in (1,2,3):
   ...    p.send(v)
   ...
   >>> results
   [2,3,4] 

The context parameter passed to the data operations callables is meant for
sharing state between them. It can be initialized to desired value(s) by passing
it to the Piper class as a (optional) keyword argument. The context parameter can
be anything; a dictionary is recommended.

Please see the tests for more examples.
