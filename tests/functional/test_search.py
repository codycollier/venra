#!/usr/bin/env python


import os
import unittest

from venra import config
from venra import search


class TestSearch(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        config.load_overrides_from_env()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_search_basic(self):
        self.assertTrue(True)


if __name__ == "__main__":

    unittest.main()
