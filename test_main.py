import unittest
from main import readRLInput, inverse_kinematics

class TestMain(unittest.TestCase):
    
    def test_inverse_kinematics(self):
        self.assertEqual((500,500), (82.3485, 123.4872))
