import unittest

from src.keycap import Keycap


class TestKeycap(unittest.TestCase):
    """Unit tests for the Keycap class"""

    def test_keycap_initialization_defaults(self):
        """Test keycap initialization with default values"""
        keycap = Keycap(name="test_keycap")

        # Test default values
        self.assertEqual(keycap.key_profile, "riskeycap")
        self.assertEqual(keycap.key_height, 8)
        self.assertEqual(keycap.wall_thickness, 1.125)
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
            legends=["A", "B"],
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
            name="test", key_profile="riskeycap", legends=["A"], render=["keycap", "stem"]
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
        self.assertIn('"\'"\'"\'"', result)  # Properly escaped single quote

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
            legends=["TEST"],
        )

        command = str(keycap)
        self.assertIn('KEY_PROFILE="dsa"', command)
        self.assertIn("KEY_HEIGHT=9.0", command)
        self.assertIn("KEY_LENGTH=18.25", command)
        self.assertIn("DISH_DEPTH=1.0", command)
        self.assertIn("WALL_THICKNESS=1.5", command)
        self.assertIn('LEGENDS=["TEST"]', command)


class TestKeycapEdgeCases(unittest.TestCase):
    """Test edge cases and special functionality for Keycap class"""

    def test_empty_legends_list(self):
        """Test with empty legends list"""
        keycap = Keycap(legends=[])
        self.assertEqual(keycap.legends, [])

    def test_multiple_legends(self):
        """Test with multiple legends"""
        legends = ["A", "1", "!"]
        keycap = Keycap(legends=legends)
        self.assertEqual(keycap.legends, legends)

    def test_special_character_legends(self):
        """Test legends with special characters"""
        legends = ["@", "#", "$", "%", "&"]
        keycap = Keycap(legends=legends)
        self.assertEqual(keycap.legends, legends)

    def test_zero_values_for_dimensions(self):
        """Test with zero dimensions"""
        keycap = Keycap(
            key_height=0,
            dish_depth=0,
            wall_thickness=0
        )
        self.assertEqual(keycap.key_height, 0)
        self.assertEqual(keycap.dish_depth, 0)
        self.assertEqual(keycap.wall_thickness, 0)

    def test_negative_values_handling(self):
        """Test with negative values (should be allowed as they are parameters)"""
        keycap = Keycap(
            key_height=-1.0,
            dish_depth=-0.5,
            wall_thickness=-0.1
        )
        self.assertEqual(keycap.key_height, -1.0)
        self.assertEqual(keycap.dish_depth, -0.5)
        self.assertEqual(keycap.wall_thickness, -0.1)

    def test_colorscad_integration(self):
        """Test command generation with colorscad path"""
        keycap = Keycap(
            name="color_test",
            colorscad_path="/path/to/colorscad.sh"
        )

        # Check that the colorscad_path is properly stored
        self.assertEqual(keycap.colorscad_path, "/path/to/colorscad.sh")

        # The actual command generation will only use it if the file exists
        command = str(keycap)
        # Command should still work normally since the file doesn't exist
        self.assertIn("openscad", command)

    def test_file_type_variations(self):
        """Test different file type outputs"""
        for file_type in ["stl", "3mf", "amf"]:
            keycap = Keycap(name="test", file_type=file_type)
            command = str(keycap)
            self.assertIn(f"test.{file_type}'", command)

    def test_render_options(self):
        """Test different render options"""
        test_cases = [
            (["keycap"], '["keycap"]'),
            (["stem"], '["stem"]'),
            (["legends"], '["legends"]'),
            (["keycap", "stem"], '["keycap", "stem"]'),
            (["keycap", "legends"], '["keycap", "legends"]'),
            (["stem", "legends"], '["stem", "legends"]'),
            (["keycap", "stem", "legends"], '["keycap", "stem", "legends"]'),
        ]

        for render_option, expected_json in test_cases:
            with self.subTest(render_option=render_option):
                keycap = Keycap(name="render_test", render=render_option)
                command = str(keycap)
                self.assertIn(f"RENDER={expected_json}", command)


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


if __name__ == "__main__":
    unittest.main()
