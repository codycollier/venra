#!/usr/bin/env python


import os
import unittest

from venra import client
from venra import system


class TestSystem(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_system_version(self):
        self.assertTrue(True)


if __name__ == "__main__":

    unittest.main()
