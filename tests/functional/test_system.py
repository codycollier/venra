#!/usr/bin/env python


import os
import unittest

from venra import client
from venra import config
from venra import system


class TestSystem(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        config.load_overrides_from_env()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_version(self):
        version_app = system.version_app()
        version_cfg = system.version_cfg()
        self.assertEqual(version_app.count("."), 2)
        self.assertEqual(version_cfg.count("."), 2)


if __name__ == "__main__":

    unittest.main()
