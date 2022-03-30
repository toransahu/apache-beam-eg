#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2022-03-17 10:58

"""Etl."""

import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from example.utils.beam_utils import ETLOption, WordExtractingDoFn
from excel2json import __author__ as e2j_author
from sample import whoami


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


logger = logging.getLogger(__name__)


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
            output | 'Write' >> beam.io.WriteToText(etl_options.output, header=whoami, footer=f"\nthanks for reading,\n{e2j_author}")


if __name__ == "__main__":
    pipeline = ETL()
    pipeline.run()
