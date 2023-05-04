#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
this_dir = Path(__file__).resolve().parent


class Pipeline:
    def run(self, args=None):
        pipeline_options = PipelineOptions([], streaming=True)
        with beam.Pipeline(options=pipeline_options) as pipeline:
            _ = (
                pipeline
                | "Create" >> beam.Create([1, 2, 3, 4, 5])
                | "BatchProcess" >> beam.ParDo(BatchUsingSetupTeardownDoFn())
            )


class BatchUsingSetupTeardownDoFn(beam.DoFn):
    def setup(self):
        self.batch = []
        logger.info(f"Setup: {self.batch}")
        return super().setup()

    def process(self, element):
        """Returns an iterator over the words of this element."""
        logger.info(f"Rx: {element}")
        self.batch.append(element)
        yield element

    def teardown(self):
        logger.info(f"Teardown: {self.batch}")
        return super().teardown()


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
