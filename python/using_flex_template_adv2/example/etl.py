#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Etl."""

import argparse
import logging
from pathlib import Path

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from example.utils.beam_utils import AuthorMessageDoFn, WordExtractingDoFn


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
                repo_root, 'results/python/examples/using_flex_template_adv2/output')),
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

            (
                pipeline
                | "EmptyPCollection" >> beam.Create([None])
                | "GetAuthorMessage" >> beam.ParDo(AuthorMessageDoFn())
                | "WriteAuthoMessage" >> beam.io.WriteToText(f"{known_args.output}.meta")
             )


if __name__ == "__main__":
    pipeline = ETL()
    pipeline.run()
