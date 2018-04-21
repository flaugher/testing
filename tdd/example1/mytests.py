import unittest
from mycode import *

class MyFirstTests(unittest.TestCase):

    def test_hello(self):
        print("testing")
        self.assertEqual(hello_world(), 'hello world')

    def test_custom_num_list(self):
        self.assertEqual(len(create_num_list(10)), 10)

if __name__ == '__main__':
    unittest.main()
