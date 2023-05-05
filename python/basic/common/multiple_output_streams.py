#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import apache_beam as beam
from apache_beam.pvalue import TaggedOutput
from apache_beam.options.pipeline_options import PipelineOptions

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Pipeline:
    def run(self, args=None):
        pipeline_options = PipelineOptions([], streaming=True)
        with beam.Pipeline(options=pipeline_options) as pipeline:
            input = pipeline | "Create1" >> beam.Create([1, 2, 3, 4, 5])

            # WAY 1
            dummy_fn_out1 = input | "DummyFn1" >> beam.ParDo(DummyFn()).with_outputs(
                "even",
                "odd",
                main="main",  # you can name the main output stream (optional)
            )
            _ = dummy_fn_out1["even"] | "LogEven1" >> beam.ParDo(LogFn())  # can be subscritable
            _ = dummy_fn_out1.odd | "LogOdd1" >> beam.ParDo(LogFn())  # can be dot-operated
            _ = dummy_fn_out1.main | "LogMain1" >> beam.ParDo(LogFn())

            # WAY 2
            # could be unpacked into no. of streams available;
            # where main stream is the first element of the tuple
            main, even, odd = input | "DummyFn2" >> beam.ParDo(DummyFn()).with_outputs(
                "even",
                "odd",
                main="main",  # you can set this if there is MAIN OUTPUT STREAM AVAILABLE
            )
            _ = even | "LogEven2" >> beam.ParDo(LogFn())
            _ = odd | "LogOdd2" >> beam.ParDo(LogFn())
            _ = main | "LogMain2" >> beam.ParDo(LogFn())

            # WAY 3
            main, even, odd = input | "DummyFn3" >> beam.ParDo(DummyWithoutMainFn()).with_outputs(
                "even",
                "odd",
                main="main",  # you can set this if there is NO main output stream available AS WELL
                # BUT the stream will be EMPTY
                # NOTE: If you do NOT set the main stream here, you CAN'T UNPACK it as well
            )
            _ = even | "LogEven3" >> beam.ParDo(LogFn())
            _ = odd | "LogOdd3" >> beam.ParDo(LogFn())
            _ = main | "LogMain3" >> beam.ParDo(LogFn())


class LogFn(beam.DoFn):
    def process(self, element):
        logger.info(f"Rx: {element} ({type(element)})")


class DummyFn(beam.DoFn):
    def process(self, element):
        if element % 2 == 0:
            yield TaggedOutput("even", element)
            return
        yield TaggedOutput("odd", element)
        yield element  # this is the main output stream


class DummyWithoutMainFn(beam.DoFn):
    def process(self, element):
        if element % 2 == 0:
            yield TaggedOutput("even", element)
            return
        yield TaggedOutput("odd", element)
        # this is without main output stream


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
