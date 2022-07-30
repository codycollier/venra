#!/usr/bin/env python


import os
import unittest

from venra import client


class TestClient(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_client_defaults(self):
        self.assertEqual(client.vclient, None)


if __name__ == "__main__":

    unittest.main()
