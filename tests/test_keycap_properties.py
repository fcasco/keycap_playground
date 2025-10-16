import unittest
from scripts.keycap import Keycap


class TestKeycapProperties(unittest.TestCase):
    """Test keycap properties and invariants"""

    def test_keycap_name_persistence(self):
        """Test that name remains consistent after initialization"""
        name = "test_name"
        keycap = Keycap(name=name)
        self.assertEqual(keycap.name, name)

    def test_legends_parameter_preservation(self):
        """Test that legends are preserved in the object"""
        legends = ["A", "B", "C"]
        keycap = Keycap(legends=legends)
        self.assertEqual(keycap.legends, legends)

    def test_parameter_bounds(self):
        """Test that parameters maintain reasonable bounds"""
        keycap = Keycap(
            key_height=5.0,  # Reasonable key height
            wall_thickness=0.5,  # Reasonable wall thickness
            dish_depth=0.8  # Reasonable dish depth
        )

        self.assertGreater(keycap.key_height, 0)
        self.assertGreater(keycap.wall_thickness, 0)
        self.assertGreaterEqual(keycap.dish_depth, 0)

    def test_command_contains_key_elements(self):
        """Test that generated commands contain key elements"""
        keycap = Keycap(name="cmd_test", key_profile="dsa", legends=["X"])
        command = str(keycap)

        # Basic elements should be present
        self.assertIn("-o", command)
        self.assertIn("cmd_test", command)
        self.assertIn("KEY_PROFILE", command)
        self.assertIn("DSA", command.upper())
        self.assertIn("LEGENDS", command)

    def test_default_render_includes_keycap(self):
        """Test that default render includes keycap"""
        keycap = Keycap(name="default_render")
        self.assertIn("keycap", keycap.render)

    def test_render_parameter_preservation(self):
        """Test that render parameter is preserved in output"""
        test_cases = [
            (["keycap"], '["keycap"]'),
            (["stem"], '["stem"]'),
            (["legends"], '["legends"]'),
            (["keycap", "stem"], '["keycap", "stem"]'),
        ]

        for render_option, expected_json in test_cases:
            with self.subTest(render_option=render_option):
                keycap = Keycap(name="render_test", render=render_option)
                command = str(keycap)
                self.assertIn(f"RENDER={expected_json}", command)
