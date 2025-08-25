
import unittest
import sys
import os
import numpy as np

# Add the parent directory to the sys.path to allow imports from the modules folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.kinematics import KinematicsCalculator

class TestKinematicsCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = KinematicsCalculator()

    def test_calculate_mru(self):
        # Test case 1: Calculate final position
        params = {'v0': 10, 't': 5, 'x0': 0}
        result = self.calculator.calculate_mru(params)
        self.assertAlmostEqual(result['calculated_values']['x'], 50)

        # Test case 2: Calculate velocity
        params = {'x': 100, 't': 10, 'x0': 0}
        result = self.calculator.calculate_mru(params)
        self.assertAlmostEqual(result['calculated_values']['v0'], 10)

        # Test case 3: Calculate time
        params = {'x': 100, 'v0': 20, 'x0': 0}
        result = self.calculator.calculate_mru(params)
        self.assertAlmostEqual(result['calculated_values']['t'], 5)

    def test_calculate_mrua(self):
        # Test case 1: Calculate final position and velocity
        params = {'v0': 10, 'a': 2, 't': 5, 'x0': 0}
        result = self.calculator.calculate_mrua(params)
        self.assertAlmostEqual(result['calculated_values']['x'], 75)
        self.assertAlmostEqual(result['calculated_values']['v'], 20)

        # Test case 2: Calculate time and final velocity
        params = {'v0': 0, 'a': 10, 'x': 500, 'x0': 0}
        result = self.calculator.calculate_mrua(params)
        self.assertAlmostEqual(result['calculated_values']['t'], 10)
        self.assertAlmostEqual(result['calculated_values']['v'], 100)

    def test_calculate_parabolic_motion(self):
        params = {'v0': 50, 'angle': 30, 'x0': 0, 'y0': 0}
        result = self.calculator.calculate_parabolic_motion(params)
        # v0y = 50 * sin(30) = 25
        # time_of_flight = 2 * 25 / 9.81 = 5.0968
        self.assertAlmostEqual(result['calculated_values']['time_of_flight'], 5.0968, places=4)
        # max_height = (25^2) / (2 * 9.81) = 31.8552
        self.assertAlmostEqual(result['calculated_values']['max_height'], 31.8552, places=4)
        # v0x = 50 * cos(30) = 43.3012
        # range = 43.3012 * 5.0968 = 220.92
        self.assertAlmostEqual(result['calculated_values']['range'], 220.925, places=3)

    def test_calculate_meeting_point(self):
        params = {
            'obj1': {'x0': 0, 'v0': 10, 'a': 2},
            'obj2': {'x0': 50, 'v0': 5, 'a': 3}
        }
        result = self.calculator.calculate_meeting_point(params)
        # 0.5 * (2-3) * t^2 + (10-5)*t + (0-50) = 0
        # -0.5t^2 + 5t - 50 = 0
        # t^2 - 10t + 100 = 0
        # discriminant = 100 - 400 = -300 -> No real solution, so my manual calc is wrong
        # Let's re-check the problem. The code should raise a ValueError here.
        with self.assertRaises(ValueError):
            self.calculator.calculate_meeting_point(params)

        # New test case where they do meet
        params = {
            'obj1': {'x0': 0, 'v0': 20, 'a': 0},
            'obj2': {'x0': 100, 'v0': 10, 'a': 0}
        }
        result = self.calculator.calculate_meeting_point(params)
        # 20t = 100 + 10t -> 10t = 100 -> t = 10
        self.assertAlmostEqual(result['calculated_values']['tiempo_encuentro'], 10)
        # position = 20 * 10 = 200
        self.assertAlmostEqual(result['calculated_values']['posicion_encuentro'], 200)

if __name__ == '__main__':
    unittest.main()
