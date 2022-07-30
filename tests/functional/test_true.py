#!/usr/bin/env python


import unittest


class TestTrue(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_true(self):
        self.assertTrue(True)


if __name__ == "__main__":

    unittest.main()
