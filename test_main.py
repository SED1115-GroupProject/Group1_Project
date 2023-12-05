import unittest
from main import setUpPotPins, readRLInput

class TestMain(unittest.TestCase):
    def test_setUpPotPins(self):
        left_potentiometer, right_potentiometer = setUpPotPins()
        self.assertEqual(left_potentiometer, 1)
        self.assertEqual(right_potentiometer, 0)
    
    def test_readRLInput(self):
        right_val, left_val = readRLInput(1,0)
        self.assertEqual(right_val, 0)
        self.assertEqual(left_val, 1)

    def test_inverse_kinematics(self):
        self.assertEqual(1, 1)
