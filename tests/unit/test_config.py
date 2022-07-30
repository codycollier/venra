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

    def test_config_defaults(self):
        reload(config)
        self.assertEqual(config.vespa_host_cfg, "http://127.0.0.1:19071")
        self.assertEqual(config.vespa_host_app, "http://127.0.0.1:8080")

    def test_config_override_env(self):

        os.environ["VESPA_HOST_CFG"] = "http://10.0.0.1:19073"
        os.environ["VESPA_HOST_APP"] = "http://10.0.0.1:8083"

        # assert defaults before override
        reload(config)
        self.assertEqual(config.vespa_host_cfg, "http://127.0.0.1:19071")
        self.assertEqual(config.vespa_host_app, "http://127.0.0.1:8080")

        # set and assert
        config.load_overrides_from_env()
        self.assertEqual(config.vespa_host_cfg, "http://10.0.0.1:19073")
        self.assertEqual(config.vespa_host_app, "http://10.0.0.1:8083")


if __name__ == "__main__":

    unittest.main()
