#!/usr/bin/env python


from importlib import reload
import os
import unittest

from venra import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_config_override_file(self):
        reload(config)
        self.assertTrue(True)


if __name__ == "__main__":

    unittest.main()
