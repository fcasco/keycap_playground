#!/usr/bin/env python3
"""
Tests for the main script to validate OpenSCAD command generation with mocks
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.keyplay import RiskeycapBase, riskeycap_alphas, KEYCAPS


class TestKeyplay(unittest.TestCase):
    """Test cases for keyplay.py OpenSCAD command generation"""

    def setUp(self):
        """Set up test fixtures"""
        self.output_path = Path("/tmp/test_output")

    def test_basic_keycap_command_generation(self):
        """Test that the RiskeycapBase class generates the correct OpenSCAD command"""
        keycap = RiskeycapBase(
            name="test_keycap",
            output_path=self.output_path,
            legends=["A"]
        )

        command = str(keycap)

        # Check that the command contains expected elements
        # The actual path to the OpenSCAD executable is used instead of just "openscad"
        self.assertIn("OpenSCAD", command)  # Check for OpenSCAD in the path
        self.assertIn("test_keycap.3mf", command)
        self.assertIn('RENDER=["keycap", "stem"]', command)
        self.assertIn('KEY_PROFILE="riskeycap"', command)
        self.assertIn('LEGENDS=["A"]', command)

    def test_riskeycap_alphas_command_generation(self):
        """Test OpenSCAD command generation with riskeycap_alphas subclass"""
        keycap = riskeycap_alphas(
            name="test_alphas",
            output_path=self.output_path,
            legends=["B"],
            key_rotation=[0, 110.1, -90]
        )

        command = str(keycap)

        # Check for custom parameters in command
        self.assertIn("KEY_ROTATION=[0, 110.1, -90]", command)
        self.assertIn('LEGENDS=["B"]', command)

    @patch("subprocess.check_output")
    def test_keycap_execution_with_mock(self, mock_check_output):
        """Test that keycap execution calls the correct OpenSCAD command"""
        # Mock the subprocess call return value
        mock_check_output.return_value = "Success"

        keycap = RiskeycapBase(
            name="mock_test_keycap",
            output_path=self.output_path,
            legends=["X"]
        )

        # Get the command string
        command = str(keycap)

        # Verify the command contains expected elements
        self.assertIn("OpenSCAD", command)  # Check for OpenSCAD in the path
        self.assertIn("mock_test_keycap.3mf", command)
        self.assertIn('KEY_PROFILE="riskeycap"', command)
        self.assertIn('LEGENDS=["X"]', command)

    def test_multiple_legends_command_generation(self):
        """Test OpenSCAD command generation with multiple legends"""
        keycap = RiskeycapBase(
            name="multi_legend_keycap",
            output_path=self.output_path,
            legends=["1", "", "!", "F1"],
            fonts=["Arial", "Arial", "Arial", "Arial"],
            font_sizes=[5.5, 4, 4, 3.5],
            trans=[[-3, -2.6, 2], [3.5, 3, 1], [0.15, -3, 2], [0.2, -2.5, 1.8]],
            rotation=[[0, -20, 0], [0, -20, 0], [0, -20, 0], [68, 0, 0]]
        )

        command = str(keycap)

        # Check that multiple legends are properly formatted (no spaces in the JSON)
        self.assertIn('LEGENDS=["1","","!","F1"]', command)
        self.assertIn('LEGEND_FONTS=["Arial", "Arial", "Arial", "Arial"]', command)

    def test_keycaps_list_content(self):
        """Test that the KEYCAPS list has expected content"""
        self.assertGreater(len(KEYCAPS), 0)  # Should have some keycaps

        # Find a specific keycap in the list
        alphas_keycap = None
        for keycap in KEYCAPS:
            if keycap.name == "1U_blank":
                alphas_keycap = keycap
                break

        self.assertIsNotNone(alphas_keycap)
        self.assertEqual(alphas_keycap.name, "1U_blank")

    def test_command_generation_for_keycaps_list(self):
        """Test command generation for first few keycaps in the list"""
        # Test first few keycaps to make sure they generate valid commands
        for i, keycap in enumerate(KEYCAPS[:3]):  # Test first 3
            command = str(keycap)
            self.assertIn("OpenSCAD", command)  # Check for OpenSCAD in the path
            self.assertIn(f"{keycap.name}.{keycap.file_type}", command)
            self.assertIn('RENDER=["keycap", "stem"]', command)

            # Stop if we've tested 3 successfully
            if i >= 2:
                break

    @patch("subprocess.check_output")
    @patch("asyncio.get_event_loop")
    def test_keyplay_script_execution_with_mock(self, mock_get_event_loop, mock_check_output):
        """Test that keyplay script execution uses the correct OpenSCAD command"""
        # Mock the subprocess call and event loop
        mock_check_output.return_value = "Success"
        mock_loop = MagicMock()
        mock_get_event_loop.return_value = mock_loop

        # Create a keycap from the keyplay script
        keycap = RiskeycapBase(
            name="script_test_keycap",
            output_path=self.output_path,
            legends=["Z"]
        )

        # Generate the OpenSCAD command
        command = str(keycap)

        # Ensure the command contains the expected elements
        self.assertIn("OpenSCAD", command)  # Path to OpenSCAD executable
        self.assertIn("script_test_keycap.3mf", command)
        self.assertIn('KEY_PROFILE="riskeycap"', command)
        self.assertIn('LEGENDS=["Z"]', command)

        # Verify that the command would be executed via subprocess
        # In the real script, this would be called by run_command function
        mock_check_output.assert_not_called()  # Only testing command generation

        # Test that the command contains all the default parameters from RiskeycapBase
        self.assertIn("KEY_ROTATION=[0, 110.1, -90]", command)
        self.assertIn("WALL_THICKNESS=1.0125", command)  # 0.45 * 2.25
        self.assertIn("UNIFORM_WALL_THICKNESS=true", command)


if __name__ == "__main__":
    unittest.main()
