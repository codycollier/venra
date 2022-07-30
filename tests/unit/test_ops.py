#!/usr/bin/env python


import os
import unittest

from venra import client
from venra import ops


class TestOps(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_ops_version(self):
        # todo: mock client
        # version_cfg = ops.version_cfg()
        # version_app = ops.version_app()
        pass


if __name__ == "__main__":

    unittest.main()
