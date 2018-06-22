import sys
import unittest
import StringIO
import diskspace
import os
from mock import patch
import argparse



class TestDiskpaceMethods(unittest.TestCase):
    def setUp(self):
        self.abs_directory = os.path.abspath('.')
        self.cmd = 'du '
        self.cmd += self.abs_directory
        self.file_tree = {self.abs_directory: {'print_size': '5.00Mb','children': [], 'size': 8}}
        self.largest_size = 24
        self.total_size = 8

    def test_print(self):
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        diskspace.print_tree(self.file_tree, self.file_tree[self.abs_directory], self.abs_directory,
                self.largest_size, self.total_size)
        sys.stdout = sys.__stdout__ 
        self.assertEqual('5.00Mb  100%  '+self.abs_directory,capturedOutput.getvalue().strip())
        
    def test_subprocess_check_output(self):
        folder = diskspace.subprocess_check_output(self.cmd)
        self.assertIn(self.abs_directory, folder)

    def test_bytes_to_readable(self):
        result = diskspace.bytes_to_readable(15986472)
        self.assertEqual(result,'7.62Gb')






if __name__ == '__main__':
    unittest.main()