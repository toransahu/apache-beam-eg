#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2022-03-30 18:47

"""Run."""


from example.etl import ETL

__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


if __name__ == "__main__":
    pipeline = ETL()
    pipeline.run()
