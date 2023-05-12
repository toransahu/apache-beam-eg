#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import time

import apache_beam as beam
import requests
from apache_beam.options.pipeline_options import (PipelineOptions,
                                                  ProfilingOptions)

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
)


class Pipeline:
    def run(self, args=None):
        pipeline_options = PipelineOptions(
            args,
            streaming=False,
            # direct_running_mode="in_memory",
            direct_running_mode="multi_threading",
            direct_num_workers=10,  # try making it 10
            profile_cpu=True,
            profile_location="./profile_dump/"
        )
        logger.info(pipeline_options.view_as(ProfilingOptions))
        with beam.Pipeline(options=pipeline_options) as pipeline:
            pcoll1 = pipeline | "Create1" >> beam.Create([1, 2, 3, 4, 5])
            pcoll2 = pipeline | "Create2" >> beam.Create(['6', '7', 8, '9', '10'])
            merged = (pcoll1, pcoll2) | 'Merge PCollections' >> beam.Flatten()
            _ = merged | "Shuffle" >> beam.Reshuffle() | "DummyFn" >> beam.ParDo(DummyFn())


class DummyFn(beam.DoFn):
    def process(self, element):
        requests.get(f"https://reqres.in/api/users?delay={element}")
        logger.info(f"Rx: {element} ({type(element)})")
        yield element


if __name__ == "__main__":
    t0 = time()
    pipeline = Pipeline()
    pipeline.run()
    elasped = time() - t0
    logger.info(f"elasped: {elasped}")
