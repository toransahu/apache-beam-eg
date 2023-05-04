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
                | "Create" >> beam.Create(range(1000))
                | "BatchProcess" >> beam.ParDo(BatchUsingStartFinishBundleDoFn())
            )


class BatchUsingStartFinishBundleDoFn(beam.DoFn):
    # NOTE: Bundle sizes are dynamically determined by the implementation of the runner based on what's currently happening inside the pipeline and its workers. In stream mode, bundles are often small in size. Dataflow bundling is influenced by backend factors like sharding usage, how much data is available for a particular key, and the throughput of the pipeline.
    # REF: https://cloud.google.com/dataflow/docs/tutorials/ecommerce-java#micro-batch-calls
    def start_bundle(self):
        self.batch = []
        logger.info(f"Start bundle: {self.batch}")
        return super().start_bundle()

    def process(self, element):
        """Returns an iterator over the words of this element."""
        logger.info(f"Rx: {element}")
        self.batch.append(element)
        yield element

    def finish_bundle(self):
        logger.info(f"Finish bundle: {self.batch}")
        return super().finish_bundle()


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
