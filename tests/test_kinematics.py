"""
Unit tests for the KinematicsCalculator class.
"""

import unittest
import sys
import os
import numpy as np

# Add the project root to the Python path to allow imports from the 'modules' directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.kinematics import KinematicsCalculator

class TestKinematicsCalculator(unittest.TestCase):
    """Test suite for the KinematicsCalculator."""

    def setUp(self):
        """Set up the test fixture."""
        self.calculator = KinematicsCalculator()

    def test_calculate_mru(self):
        """Test the calculation of Uniform Rectilinear Motion."""
        # Test case 1: Calculate final position.
        params = {'v0': 10, 't': 5, 'x0': 0}
        result = self.calculator.calculate_mru(params)
        self.assertAlmostEqual(result['calculated_values']['x'], 50)

        # Test case 2: Calculate velocity.
        params = {'x': 100, 't': 10, 'x0': 0}
        result = self.calculator.calculate_mru(params)
        self.assertAlmostEqual(result['calculated_values']['v0'], 10)

        # Test case 3: Calculate time.
        params = {'x': 100, 'v0': 20, 'x0': 0}
        result = self.calculator.calculate_mru(params)
        self.assertAlmostEqual(result['calculated_values']['t'], 5)

    def test_calculate_mrua(self):
        """Test the calculation of Uniformly Accelerated Rectilinear Motion."""
        # Test case 1: Calculate final position and velocity.
        params = {'v0': 10, 'a': 2, 't': 5, 'x0': 0}
        result = self.calculator.calculate_mrua(params)
        self.assertAlmostEqual(result['calculated_values']['x'], 75)
        self.assertAlmostEqual(result['calculated_values']['v'], 20)

        # Test case 2: Calculate time and final velocity.
        params = {'v0': 0, 'a': 10, 'x': 500, 'x0': 0}
        result = self.calculator.calculate_mrua(params)
        self.assertAlmostEqual(result['calculated_values']['t'], 10)
        self.assertAlmostEqual(result['calculated_values']['v'], 100)

    def test_calculate_parabolic_motion(self):
        """Test the calculation of parabolic motion."""
        params = {'v0': 50, 'angle': 30, 'x0': 0, 'y0': 0}
        result = self.calculator.calculate_parabolic_motion(params)
        # v0y = 50 * sin(30) = 25
        # time_of_flight = 2 * 25 / 9.81 = 5.0968
        self.assertAlmostEqual(result['calculated_values']['time_of_flight'], 5.0968, places=4)
        # max_height = (25^2) / (2 * 9.81) = 31.8552
        self.assertAlmostEqual(result['calculated_values']['max_height'], 31.8552, places=4)
        # v0x = 50 * cos(30) = 43.3012
        # range = 43.3012 * 5.0968 = 220.92
        self.assertAlmostEqual(result['calculated_values']['range'], 220.6996, places=4)

    def test_calculate_meeting_point(self):
        """Test the calculation of the meeting point of two objects."""
        # Test case where they do not meet.
        params_no_meet = {
            'obj1': {'x0': 0, 'v0': 10, 'a': 2},
            'obj2': {'x0': 50, 'v0': 5, 'a': 3}
        }
        with self.assertRaises(ValueError):
            self.calculator.calculate_meeting_point(params_no_meet)

        # Test case where they do meet.
        params_meet = {
            'obj1': {'x0': 0, 'v0': 20, 'a': 0},
            'obj2': {'x0': 100, 'v0': 10, 'a': 0}
        }
        result = self.calculator.calculate_meeting_point(params_meet)
        # 20t = 100 + 10t -> 10t = 100 -> t = 10
        self.assertAlmostEqual(result['calculated_values']['meeting_time'], 10)
        # position = 20 * 10 = 200
        self.assertAlmostEqual(result['calculated_values']['meeting_position'], 200)

if __name__ == '__main__':
    unittest.main()