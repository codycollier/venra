#!/usr/bin/env python
"""Run all of the tests

This runner currently requires all test modules be imported and listed
manually.  With each run, the order of the suites is randomized.  Further,
the order of the tests inside each suite is also randomized.

"""

import unittest
import random

import test_true
import test_config
import test_client
import test_document
import test_search
import test_system
import test_visit


test_modules = (test_true, test_config, test_client, 
                test_document, test_search, test_system, test_visit)

suite_list = []
for testmod in test_modules:

    suite = unittest.TestLoader().loadTestsFromModule(testmod)

    # shuffle the list of tests in this suite
    random.shuffle(suite._tests)
    suite_list.append(suite)

# shuffle the order of the suites
random.shuffle(suite_list)

all_suites = unittest.TestSuite(suite_list)
unittest.TextTestRunner(verbosity=2).run(all_suites)

