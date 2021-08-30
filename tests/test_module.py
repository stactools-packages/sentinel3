import unittest

import stactools.sentinel3


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.sentinel3.__version__)
