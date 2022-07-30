#!/usr/bin/env python


import os
import unittest

from venra import client
from venra import config
from venra import ops


class TestOps(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        config.load_overrides_from_env()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_ops_version(self):
        version_app = ops.version_app()
        version_cfg = ops.version_cfg()
        self.assertEqual(version_app.count("."), 2)
        self.assertEqual(version_cfg.count("."), 2)


if __name__ == "__main__":

    unittest.main()
