import unittest
from inverse_kinematics import inverse_kinematics

class TestMain(unittest.TestCase):
    
    def test_inverse_kinematics(self):
        self.assertAlmostEqual((500,500), (82.3485, 123.4872))


if __name__ == '__main__':
    unittest.main()
