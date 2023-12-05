import unittest
from main import readRLInput, inverse_kinematics

class TestMain(unittest.TestCase):
    
    def test_readRLInput(self):
        right_val, left_val = readRLInput(1,0)
        self.assertEqual(right_val, 0)
        self.assertEqual(left_val, 1)

    def test_inverse_kinematics(self):
        self.assertEqual((500,500), (82.3485, 123.4872))
