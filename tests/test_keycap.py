import unittest
from scripts.keycap import Keycap


class TestKeycap(unittest.TestCase):
    """Unit tests for the Keycap class"""

    def test_keycap_initialization_defaults(self):
        """Test keycap initialization with default values"""
        keycap = Keycap(name="test_keycap")

        # Test default values
        self.assertEqual(keycap.key_profile, "riskeycap")
        self.assertEqual(keycap.key_height, 8)
        self.assertEqual(keycap.wall_thickness, 0.45 * 2.5)
        self.assertEqual(keycap.uniform_wall_thickness, True)
        self.assertEqual(keycap.legends, [""])
        self.assertEqual(keycap.name, "test_keycap")

    def test_keycap_initialization_with_custom_params(self):
        """Test keycap initialization with custom parameters"""
        keycap = Keycap(
            name="custom_keycap",
            key_profile="dsa",
            key_height=9,
            wall_thickness=2.0,
            legends=["A", "B"]
        )

        self.assertEqual(keycap.key_profile, "dsa")
        self.assertEqual(keycap.key_height, 9)
        self.assertEqual(keycap.wall_thickness, 2.0)
        self.assertEqual(keycap.legends, ["A", "B"])
        self.assertEqual(keycap.name, "custom_keycap")

    def test_keycap_name_generation_from_legend(self):
        """Test that keycap name is set from legend when not explicitly provided"""
        keycap = Keycap(legends=["Q"])
        self.assertEqual(keycap.name, "Q")

    def test_keycap_name_generation_default(self):
        """Test that keycap name defaults to 'keycap' when no legend provided"""
        keycap = Keycap(legends=[""])
        self.assertEqual(keycap.name, "keycap")

    def test_postinit_parameter_override(self):
        """Test that postinit properly overrides parameters"""
        keycap = Keycap(name="initial", key_height=8)
        keycap.postinit(key_height=10, name="updated")

        self.assertEqual(keycap.key_height, 10)
        self.assertEqual(keycap.name, "updated")

    def test_openscad_command_generation(self):
        """Test that OpenSCAD command string is generated correctly"""
        keycap = Keycap(
            name="test",
            key_profile="riskeycap",
            legends=["A"],
            render=["keycap", "stem"]
        )

        command = str(keycap)
        self.assertIn('RENDER=["keycap", "stem"]', command)
        self.assertIn('KEY_PROFILE="riskeycap"', command)
        self.assertIn('LEGENDS=["A"]', command)

    def test_quote_escaping_functionality(self):
        """Test that single quotes are properly escaped in legend lists"""
        keycap = Keycap()

        # Test single quote escaping
        result = keycap.quote(["'", "test"])
        self.assertIn("\"'\"'\"'\"", result)  # Properly escaped single quote

        # Test normal strings
        result = keycap.quote(["A", "B"])
        self.assertIn('"A","B"', result)

    def test_openscad_command_includes_all_parameters(self):
        """Test that generated command includes all major parameters"""
        keycap = Keycap(
            name="full_test",
            key_profile="dsa",
            key_height=9.0,
            key_length=18.25,
            dish_depth=1.0,
            wall_thickness=1.5,
            legends=["TEST"]
        )

        command = str(keycap)
        self.assertIn('KEY_PROFILE="dsa"', command)
        self.assertIn("KEY_HEIGHT=9.0", command)
        self.assertIn("KEY_LENGTH=18.25", command)
        self.assertIn("DISH_DEPTH=1.0", command)
        self.assertIn("WALL_THICKNESS=1.5", command)
        self.assertIn('LEGENDS=["TEST"]', command)


if __name__ == "__main__":
    unittest.main()
