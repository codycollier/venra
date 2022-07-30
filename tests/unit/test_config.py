#!/usr/bin/env python


import os
import unittest

from venra import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_config_defaults(self):
        self.assertEqual(config.vespa_host, "127.0.0.1")
        self.assertEqual(config.vespa_port_cfg, "19071")
        self.assertEqual(config.vespa_port_app, "8080")

    def test_config_override_env(self):

        os.environ["VESPA_HOST"] = "10.0.0.1"
        os.environ["VESPA_PORT_CFG"] = "19073"
        os.environ["VESPA_PORT_APP"] = "8083"

        # assert defaults before override
        self.assertEqual(config.vespa_host, "127.0.0.1")
        self.assertEqual(config.vespa_port_cfg, "19071")
        self.assertEqual(config.vespa_port_app, "8080")

        # set and assert
        config.load_overrides_from_env()
        self.assertEqual(config.vespa_host, "10.0.0.1")
        self.assertEqual(config.vespa_port_cfg, "19073")
        self.assertEqual(config.vespa_port_app, "8083")


if __name__ == "__main__":

    unittest.main()
