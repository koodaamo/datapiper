===============================
Overview
===============================

Datapiper provides an easy-to-use yet configurable data batch processing tool
and a simple framework for data integration applications.

Give Datapiper your list of data processor callables and it will construct a
runnable data pipeline for you.

Define those in the `piper.cfg` configuration file written in
YAML, you can also use 'piper run mypipename' cli tool to run your pipeline.

If you instantiate the pipe with a (iterable) data source, you get a generator
that reads from a source and outputs processed data for you.

If you instead instantiate it with a (callable) data sink, you get a coroutine
that accepts data from a producer and delivers processed data to a sink.

That's all.


