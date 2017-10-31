===============================
Overview
===============================

Datapiper provides an easy-to-use yet configurable data batch processing tool
and a simple pipeline library for use in data integration applications.

Give Datapiper your list of data processor callables and it will construct a
runnable data pipeline for you.

Define those in the `piper.cfg` configuration file written in
YAML, you can also use 'piper run mypipename' cli tool to run your pipeline.

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

That's all.


