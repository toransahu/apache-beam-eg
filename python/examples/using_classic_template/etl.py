#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2022-03-17 10:58

"""Etl."""

import argparse
from pathlib import Path
import logging
import re

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, _BeamArgumentParser


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


logger = logging.getLogger(__name__)
this_dir = Path(__file__).resolve().parent


class ETLOption(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser: _BeamArgumentParser) -> None:
        parser.add_value_provider_argument(
            '--input',
            # default='gs://dataflow-samples/shakespeare/kinglear.txt',
            default=str(Path.joinpath(
                this_dir.parent.parent.parent, 'data/input.txt')),
            help='Input file to process.',
        )
        parser.add_value_provider_argument(
            '--output',
            default=str(Path.joinpath(
                this_dir.parent.parent.parent, 'results/python/examples/using_classic_template/output')),
            help='Output file to write results to.',
        )



class ETL:
    def run(self, args=None):
        pipeline_options = PipelineOptions(args, save_main_session=True)
        etl_options = pipeline_options.view_as(ETLOption)
        with beam.Pipeline(options=pipeline_options) as pipeline:
            lines = (
                pipeline
                | "Read" >> beam.io.ReadFromText(etl_options.input)
            )
            counts = (
                lines
                | 'Split' >> (beam.ParDo(WordExtractingDoFn()).with_output_types(str))
                | 'PairLowerCaseWithOne' >> beam.Map(lambda x: (x.lower(), 1))
                | 'GroupAndSum' >> beam.CombinePerKey(sum)
            )

            # Format the counts into a PCollection of strings.
            def format_result(word, count):
                return '%s: %d' % (word, count)

            output = counts | 'Format' >> beam.MapTuple(format_result)

            # Write the output using a "Write" transform
            output | 'Write' >> beam.io.WriteToText(etl_options.output)


class WordExtractingDoFn(beam.DoFn):
    """Parse each line of input text into words."""

    def process(self, element):
        """Returns an iterator over the words of this element."""
        return re.findall(r'[\w\']+', element, re.UNICODE)


if __name__ == "__main__":
    pipeline = ETL()
    pipeline.run()
