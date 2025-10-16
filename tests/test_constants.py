"""Test constants that affect keycap generation"""
import unittest
from scripts.keycap import KEY_UNIT, BETWEENSPACE


class TestConstants(unittest.TestCase):
    """Test that constants are properly defined and used"""

    def test_key_unit_value(self):
        """Test that KEY_UNIT has the expected value"""
        self.assertEqual(KEY_UNIT, 19.05)  # Standard keyboard unit

    def test_betspace_value(self):
        """Test that BETWEENSPACE has the expected value"""
        self.assertEqual(BETWEENSPACE, 0.8)

    def test_key_unit_positive(self):
        """Test that KEY_UNIT is positive"""
        self.assertGreater(KEY_UNIT, 0)

    def test_betspace_positive(self):
        """Test that BETWEENSPACE is positive"""
        self.assertGreater(BETWEENSPACE, 0)
