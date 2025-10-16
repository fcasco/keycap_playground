import unittest
from scripts.keycap import Keycap


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


if __name__ == "__main__":
    unittest.main()
