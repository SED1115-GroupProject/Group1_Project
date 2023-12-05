import unittest
from inverse_kinematics import inverse_kinematics, translate

class TestMain(unittest.TestCase):
    
    def test_inverse_kinematics(self):
        resultX, resultY = inverse_kinematics(150,200)
        self.assertAlmostEqual(resultX, 81.58723, delta=1)
        self.assertAlmostEqual(resultY, 123.1523, delta=1)
      
    
    def test_translate(self):
        self.assertAlmostEqual(translate(0), 1638)


if __name__ == '__main__':
    unittest.main()
