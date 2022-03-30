#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Etl."""

import argparse
from pathlib import Path
import logging
import re

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


logger = logging.getLogger(__name__)
this_dir = Path(__file__).resolve().parent
repo_root = this_dir.parent.parent.parent


class ETL:
    def run(self, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--input',
            # default='gs://dataflow-samples/shakespeare/kinglear.txt',
            default=str(Path.joinpath(
                repo_root, 'data/input.txt')),
            help='Input file to process.',
        )
        parser.add_argument(
            '--output',
            default=str(Path.joinpath(
                repo_root, 'results/python/examples/using_flex_template/output')),
            help='Output file to write results to.',
        )

        known_args, extra_args = parser.parse_known_args(args)
        pipeline_options = PipelineOptions(extra_args, save_main_session=True)
        with beam.Pipeline(options=pipeline_options) as pipeline:
            lines = (
                pipeline
                | "Read" >> beam.io.ReadFromText(known_args.input)
            )
            counts = (
                lines
                | 'Split' >> beam.ParDo(WordExtractingDoFn()).with_output_types(str)
                | 'PairLowerCaseWithOne' >> beam.Map(lambda x: (x.lower(), 1))
                | 'GroupAndSum' >> beam.CombinePerKey(sum)
            )

            # Format the counts into a PCollection of strings.
            def format_result(word, count):
                return '%s: %d' % (word, count)

            output = counts | 'Format' >> beam.MapTuple(format_result)
            # Write the output using a "Write" transform
            output | 'Write' >> beam.io.WriteToText(known_args.output)


class WordExtractingDoFn(beam.DoFn):
    """Parse each line of input text into words."""

    def process(self, element):
        """Returns an iterator over the words of this element."""
        return re.findall(r'[\w\']+', element, re.UNICODE)


if __name__ == "__main__":
    pipeline = ETL()
    pipeline.run()
