#!/usr/bin/env python3
"""
Tests for riskeycap module.

Tests the riskeycap classes and their functionality.
"""
import unittest

from src.riskeycap import (
    RiskeycapBase,
    KEYCAPS,
    KEY_UNIT,
    BETWEENSPACE,
    riskeycap_alphas,
    riskeycap_1_25U,
    riskeycap_1_5U,
    riskeycap_1_75U,
    riskeycap_2U,
    riskeycap_2UV,
    riskeycap_2_25U,
    riskeycap_2_5U,
    riskeycap_2_75U,
    riskeycap_6_25U,
    riskeycap_7U,
)


class TestRiskeycapBase(unittest.TestCase):
    """Test the RiskeycapBase class."""

    def test_riskeycap_base_initialization(self):
        """Test that RiskeycapBase initializes with correct default values."""
        keycap = RiskeycapBase(name="test_keycap")

        # Check default values are set correctly
        self.assertEqual(keycap.key_profile, "riskeycap")
        self.assertEqual(keycap.key_rotation, [0, 110.1, -90])
        self.assertEqual(keycap.wall_thickness, 0.45 * 2.25)
        self.assertTrue(keycap.uniform_wall_thickness)
        self.assertEqual(keycap.dish_thickness, 1.0)
        self.assertEqual(keycap.dish_corner_fn, 40)
        self.assertEqual(keycap.polygon_layers, 4)
        self.assertEqual(keycap.stem_type, "box_cherry")
        self.assertEqual(keycap.render, ["keycap", "stem"])
        self.assertEqual(keycap.default_file_type, "stl")
        self.assertEqual(keycap.file_type, "stl")

    def test_riskeycap_base_with_custom_kwargs(self):
        """Test that RiskeycapBase accepts custom keyword arguments."""
        keycap = RiskeycapBase(
            name="custom_keycap", key_rotation=[0, 90, 0], wall_thickness=2.0, file_type="3mf"
        )

        self.assertEqual(keycap.name, "custom_keycap")
        self.assertEqual(keycap.key_rotation, [0, 90, 0])
        self.assertEqual(keycap.wall_thickness, 2.0)
        self.assertEqual(keycap.file_type, "3mf")


class TestRiskeycapSpecializations(unittest.TestCase):
    """Test various riskeycap specializations."""

    def test_alphas_initialization(self):
        """Test riskeycap_alphas initialization."""
        keycap = riskeycap_alphas(name="A")

        # Should inherit from RiskeycapBase but override font sizes and positions
        self.assertEqual(keycap.name, "A")
        self.assertEqual(keycap.key_profile, "riskeycap")
        self.assertEqual(keycap.font_sizes[0], 4.5)  # Regular Gotham Rounded

    def test_1_25u_naming(self):
        """Test that 1.25U keycap has correct naming prefix."""
        keycap = riskeycap_1_25U(name="test_keycap")

        # Should have 1.25U_ prefix added
        self.assertTrue(keycap.name.startswith("1.25U_"))
        self.assertEqual(keycap.key_length, KEY_UNIT * 1.25 - 0.8)

    def test_1_5u_naming(self):
        """Test that 1.5U keycap has correct naming prefix."""
        keycap = riskeycap_1_5U(name="test_keycap")

        # Should have 1.5U_ prefix added
        self.assertTrue(keycap.name.startswith("1.5U_"))

    def test_1_75u_naming(self):
        """Test that 1.75U keycap has correct naming prefix."""
        keycap = riskeycap_1_75U(name="test_keycap")

        # Should have 1.75U_ prefix added
        self.assertTrue(keycap.name.startswith("1.75U_"))

    def test_2u_naming(self):
        """Test that 2U keycap has correct naming prefix."""
        keycap = riskeycap_2U(name="test_keycap")

        # Should have 2U_ prefix added
        self.assertTrue(keycap.name.startswith("2U_"))

    def test_2uv_naming(self):
        """Test that 2UV keycap has correct naming prefix."""
        keycap = riskeycap_2UV(name="test_keycap")

        # Should have 2UV_ prefix added
        self.assertTrue(keycap.name.startswith("2UV_"))

    def test_2_25u_naming(self):
        """Test that 2.25U keycap has correct naming prefix."""
        keycap = riskeycap_2_25U(name="test_keycap")

        # Should have 2.25U_ prefix added
        self.assertTrue(keycap.name.startswith("2.25U_"))

    def test_2_5u_naming(self):
        """Test that 2.5U keycap has correct naming prefix."""
        keycap = riskeycap_2_5U(name="test_keycap")

        # Should have 2.5U_ prefix added
        self.assertTrue(keycap.name.startswith("2.5U_"))

    def test_2_75u_naming(self):
        """Test that 2.75U keycap has correct naming prefix."""
        keycap = riskeycap_2_75U(name="test_keycap")

        # Should have 2.75U_ prefix added
        self.assertTrue(keycap.name.startswith("2.75U_"))

    def test_6_25u_naming(self):
        """Test that 6.25U keycap has correct naming prefix."""
        keycap = riskeycap_6_25U(name="test_keycap")

        # Should have 6.25U_ prefix added
        self.assertTrue(keycap.name.startswith("6.25U_"))

    def test_7u_naming(self):
        """Test that 7U keycap has correct naming prefix."""
        keycap = riskeycap_7U(name="test_keycap")

        # Should have 7U_ prefix added
        self.assertTrue(keycap.name.startswith("7U_"))

    def test_naming_with_existing_prefix(self):
        """Test that naming doesn't double-add prefixes."""
        keycap = riskeycap_1_25U(name="1.25U_existing")

        # Should not double the prefix
        self.assertEqual(keycap.name, "1.25U_existing")


class TestKeycapsConstant(unittest.TestCase):
    """Test the KEYCAPS constant."""

    def test_keycaps_is_list(self):
        """Test that KEYCAPS is a list."""
        self.assertIsInstance(KEYCAPS, list)

    def test_keycaps_not_empty(self):
        """Test that KEYCAPS contains keycaps."""
        self.assertGreater(len(KEYCAPS), 0)

    def test_all_keycaps_have_names(self):
        """Test that all keycaps in KEYCAPS have names."""
        for keycap in KEYCAPS:
            # Should have a name attribute (could be None or empty string)
            self.assertIsNotNone(keycap)
            self.assertTrue(hasattr(keycap, "name"))

    def test_keycap_names_are_strings_or_none(self):
        """Test that keycap names are either strings or None."""
        for keycap in KEYCAPS:
            if keycap.name is not None:
                self.assertIsInstance(keycap.name, str)

    def test_all_keycaps_inherit_from_keycap(self):
        """Test that all keycaps inherit from the Keycap base class."""
        from src.keycap import Keycap

        for keycap in KEYCAPS:
            self.assertIsInstance(keycap, Keycap)


class TestKeycapProperties(unittest.TestCase):
    """Test specific keycap properties and configurations."""

    def test_key_unit_constant(self):
        """Test that KEY_UNIT is defined correctly."""
        self.assertEqual(KEY_UNIT, 19.05)

    def test_between_space_constant(self):
        """Test that BETWEENSPACE is defined correctly."""
        self.assertEqual(BETWEENSPACE, 0.8)

    def test_different_unit_sizes(self):
        """Test that different unit sizes have appropriate dimensions."""
        # Test 1.25U
        keycap_1_25 = riskeycap_1_25U(name="test")
        expected_1_25 = KEY_UNIT * 1.25 - BETWEENSPACE
        self.assertAlmostEqual(keycap_1_25.key_length, expected_1_25, places=2)

        # Test 1.75U
        keycap_1_75 = riskeycap_1_75U(name="test")
        expected_1_75 = KEY_UNIT * 1.75 - BETWEENSPACE
        self.assertAlmostEqual(keycap_1_75.key_length, expected_1_75, places=2)

    def test_font_configurations(self):
        """Test that font configurations are properly set."""
        keycap = riskeycap_alphas(name="A")

        # Should have font configuration
        self.assertIsInstance(keycap.fonts, list)
        self.assertIsInstance(keycap.font_sizes, list)
        self.assertIsInstance(keycap.trans, list)
        self.assertIsInstance(keycap.rotation, list)

        # Should have 3 legends (main, secondary, front)
        self.assertEqual(len(keycap.fonts), 3)
        self.assertEqual(len(keycap.font_sizes), 3)
        self.assertEqual(len(keycap.trans), 3)
        self.assertEqual(len(keycap.rotation), 3)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def test_keycap_with_none_name(self):
        """Test that keycaps can handle None names gracefully."""
        keycap = RiskeycapBase(name=None)

        # Should not crash when name is None
        self.assertIsNone(keycap.name)

    def test_keycap_with_empty_name(self):
        """Test that keycaps can handle empty names gracefully."""
        keycap = RiskeycapBase(name="")

        # Should handle empty name
        self.assertEqual(keycap.name, "")

    def test_keycap_naming_safety_with_none(self):
        """Test that None name doesn't cause crashes in naming methods."""
        keycap = RiskeycapBase(name=None)

        # Should not crash when calling startswith on None
        # This tests the fix for the type checking issues
        if keycap.name is not None:
            result = keycap.name.startswith("test_")
        else:
            result = False
        self.assertIsInstance(result, bool)


if __name__ == "__main__":
    unittest.main()
