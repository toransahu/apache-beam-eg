#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2022-03-30 10:35

"""Beam Utils."""

import logging
import re

import apache_beam as beam
from excel2json import __author__ as e2j_author
from sample import whoami


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


logger = logging.getLogger(__name__)


class WordExtractingDoFn(beam.DoFn):
    """Parse each line of input text into words."""

    def process(self, element):
        """Returns an iterator over the words of this element."""
        return re.findall(r'[\w\']+', element, re.UNICODE)


class AuthorMessageDoFn(beam.DoFn):
    def process(self, element, *args, **kwargs):
        msg = [f"{whoami}\nthanks for reading,\n{e2j_author}"]
        return msg
