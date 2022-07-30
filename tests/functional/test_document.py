#!/usr/bin/env python


import os
import unittest

from venra import config
from venra import document


class TestDocument(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        config.load_overrides_from_env()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_doc_get(self):
        self.assertTrue(True)


if __name__ == "__main__":

    unittest.main()
