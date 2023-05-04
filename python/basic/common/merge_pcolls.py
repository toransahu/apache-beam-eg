#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Pipeline:
    def run(self, args=None):
        pipeline_options = PipelineOptions([], streaming=True)
        with beam.Pipeline(options=pipeline_options) as pipeline:
            pcoll1 = pipeline | "Create1" >> beam.Create([1, 2, 3, 4, 5])
            pcoll2 = pipeline | "Create2" >> beam.Create(['6', '7', 8, '9', '10'])
            merged = (pcoll1, pcoll2) | 'Merge PCollections' >> beam.Flatten()
            _ = merged | "DummyFn" >> beam.ParDo(DummyFn())


class DummyFn(beam.DoFn):
    def process(self, element):
        logger.info(f"Rx: {element} ({type(element)})")
        yield element


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
