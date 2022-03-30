#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2022-03-30 10:35

"""Beam Utils."""

import logging
from pathlib import Path
import re

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, _BeamArgumentParser


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


logger = logging.getLogger(__name__)
this_dir = Path(__file__).resolve().parent
repo_root = this_dir.parent.parent.parent.parent

class WordExtractingDoFn(beam.DoFn):
    """Parse each line of input text into words."""

    def process(self, element):
        """Returns an iterator over the words of this element."""
        return re.findall(r'[\w\']+', element, re.UNICODE)


class ETLOption(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser: _BeamArgumentParser) -> None:
        parser.add_value_provider_argument(
            '--input',
            # default='gs://dataflow-samples/shakespeare/kinglear.txt',
            default=str(Path.joinpath(
                repo_root, 'data/input.txt')),
            help='Input file to process.',
        )
        parser.add_value_provider_argument(
            '--output',
            default=str(Path.joinpath(
                repo_root, 'results/python/examples/using_classic_template_adv1/output')),
            help='Output file to write results to.',
        )
