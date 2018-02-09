import unittest
import sys
from common.utils import pre_process_text, get_run_key
from datetime import datetime

class TestUtils(unittest.TestCase):
    def test_1(self):
        self.assertEqual(pre_process_text('multiple\nlines\n'), 'multiple lines ')

    def test_2(self):
        self.assertEqual(pre_process_text('&gt;multiple &gt;lines'), '>multiple >lines')

    def test_3(self):
        self.assertEqual(pre_process_text('It removes links http://some.url'), 'It removes links ')

if __name__ == '__main__':
   unittest.main()
