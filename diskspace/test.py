import sys
import unittest
import StringIO
import diskspace
import os

class TestDiskpaceMethods(unittest.TestCase):
    def setUp(self):
        self.abs_directory = os.path.abspath('.')
        self.cmd = 'du '
        self.cmd += self.abs_directory
        self.file_tree = {self.abs_directory: {'print_size': '5.00Mb','children': [], 'size': 8}}
        self.file_tree_two = {self.abs_directory: {'print_size': '5.00Mb','children': [], 'size': -1}}
        self.largest_size = 24
        self.total_size = 8
       
    def test_subprocess_check_output(self):
        folder = diskspace.subprocess_check_output(self.cmd)
        self.assertIn(self.abs_directory, folder)

    def test_bytes_to_readable_zero(self):
        result = diskspace.bytes_to_readable(15986472)
        self.assertEqual(result,'7.62Gb')

    def test_bytes_to_readable(self):
        result = diskspace.bytes_to_readable(0)
        self.assertEqual(result,'0.00B')

    def test_print_tree(self):
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        diskspace.print_tree(self.file_tree, self.file_tree[self.abs_directory], self.abs_directory,
                self.largest_size, self.total_size)
        sys.stdout = sys.__stdout__ 
        self.assertEqual('5.00Mb  100%  '+self.abs_directory,capturedOutput.getvalue().strip())

    def test_print_tree_two(self):
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        diskspace.print_tree(self.file_tree, self.file_tree_two[self.abs_directory], self.abs_directory,
                self.largest_size, self.total_size)
        sys.stdout = sys.__stdout__ 
        self.assertEqual('',capturedOutput.getvalue().strip())
    
    def test_show_space_list(self):
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        diskspace.show_space_list(diskspace.args.directory, diskspace.args.depth,
                        order=(diskspace.args.order == 'desc'))
        sys.stdout = sys.__stdout__
        self.assertIn('Size (%) File' and self.abs_directory,capturedOutput.getvalue().strip())
    
    def test_calculate_percentage(self):
        self.assertEqual(50,diskspace.calculate_percentage(4,8))
    

if __name__ == '__main__':
    unittest.main()