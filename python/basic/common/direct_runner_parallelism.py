#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Setting parallelism

Number of threads or subprocesses is defined by setting the direct_num_workers pipeline option. From 2.22.0, direct_num_workers = 0 is supported. When direct_num_workers is set to 0, it will set the number of threads/subprocess to the number of cores of the machine where the pipeline is running.

# Setting running mode

In Beam 2.19.0 and newer, you can use the direct_running_mode pipeline option to set the running mode. direct_running_mode can be one of ['in_memory', 'multi_threading', 'multi_processing'].

in_memory: Runner and workers’ communication happens in memory (not through gRPC). This is a default mode.

multi_threading: Runner and workers communicate through gRPC and each worker runs in a thread.

multi_processing: Runner and workers communicate through gRPC and each worker runs in a subprocess.
"""

import logging
from time import time

import requests
import apache_beam as beam
from apache_beam.options.pipeline_options import DirectOptions, PipelineOptions

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
            # Ref: https://beam.apache.org/documentation/runners/direct/#setting-parallelism
            # direct_running_mode="in_memory",
            direct_running_mode="multi_threading",
            # FIXME: multi_processing is not working,
            # DummyFn is missing environment, all the libs,
            # even logger object from __main__
            # direct_running_mode="multi_processing",
            direct_num_workers=1,  # try making it 10
        )
        direct_opts = pipeline_options.view_as(DirectOptions)
        logger.info(direct_opts)  # take a look at DirectOptions class
        with beam.Pipeline(options=pipeline_options) as pipeline:
            pcoll1 = pipeline | "Create1" >> beam.Create([1, 2, 3, 4, 5])
            pcoll2 = pipeline | "Create2" >> beam.Create(['6', '7', 8, '9', '10'])
            merged = (pcoll1, pcoll2) | 'Merge PCollections' >> beam.Flatten()
            # NOTE: Without Reshuffle, parallelism is not gonna happen
            _ = merged | "Shuffle" >> beam.Reshuffle() | "DummyFn" >> beam.ParDo(DummyFn())


class DummyFn(beam.DoFn):
    def process(self, element):
        # This API call returns with specified delay seconds
        requests.get(f"https://reqres.in/api/users?delay={element}")
        logger.info(f"Rx: {element} ({type(element)})")
        yield element


if __name__ == "__main__":
    t0 = time()
    pipeline = Pipeline()
    pipeline.run()
    elasped = time() - t0
    logger.info(f"elasped: {elasped}")
