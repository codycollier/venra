#!/usr/bin/env python


import os
import unittest

import requests

from venra import config
from venra import client


class TestClient(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        config.load_overrides_from_env()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_client_basic(self):
        client.reset()
        self.assertEqual(client.vclient, None)
        vc = client.get_vespa_client()
        self.assertEqual(vc, client.vclient)
        self.assertEqual(type(vc), type(requests.Session()))


if __name__ == "__main__":

    unittest.main()
