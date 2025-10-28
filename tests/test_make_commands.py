"""
Tests for the make_commands function in keyplay.py
"""

from pathlib import Path
import unittest
from unittest.mock import patch

from src.keyplay import RiskeycapBase, KEYCAPS, make_commands


class MockArgs:
    def __init__(self, **kwargs):
        self.out = kwargs.get("out", "/tmp/test_output")
        self.names = kwargs.get("names", None)
        self.legends = kwargs.get("legends", False)
        self.force = kwargs.get("force", False)
        self.file_type = kwargs.get("file_type", "stl")


class TestMakeCommandsFunction(unittest.TestCase):
    """Test the make_commands function from keyplay module"""

    def setUp(self):
        """Set up test fixtures"""
        self.output_path = Path("/tmp/test_output")

    def test_make_commands_basic_single_keycap(self):
        """Test make_commands with a single keycap using default parameters"""
        # Create a simple keycap for testing
        test_keycap = RiskeycapBase(
            name="test_keycap", output_path=str(self.output_path), legends=["A"]
        )

        # Temporarily add it to KEYCAPS for this test
        original_keycaps = list(KEYCAPS)  # Make a copy
        KEYCAPS.clear()
        KEYCAPS.append(test_keycap)

        try:
            # Create args with default parameters
            args = MockArgs(names=["test_keycap"], force=True)

            # Call make_commands
            commands = make_commands(args)

            # Check that we got commands
            self.assertGreater(len(commands), 0, "Should generate at least one command")

            # Check that the command contains expected elements
            command_str = str(commands[0])
            self.assertIn("test_keycap", command_str)
            self.assertIn(".stl", command_str)
            self.assertIn('RENDER=["keycap", "stem"]', command_str)
            self.assertIn('LEGENDS=["A"]', command_str)
        finally:
            # Restore original KEYCAPS
            KEYCAPS.clear()
            KEYCAPS.extend(original_keycaps)

    def test_make_commands_all_keycaps(self):
        """Test make_commands processes all keycaps when no specific names are provided"""
        args = MockArgs(names=None, force=True)

        # Call make_commands
        commands = make_commands(args)

        # Check that we got commands for all keycaps
        self.assertGreater(len(commands), 0, "Should generate commands for all keycaps")

        # Check that each command is a string
        for command in commands:
            self.assertIsInstance(command, str, "Each command should be a string")
            self.assertIn(".stl", command, "Default file type should be .stl")

    def test_make_commands_specific_keycap_names(self):
        """Test make_commands processes only specific keycap names when provided"""
        # Find a keycap that exists in the KEYCAPS list
        if len(KEYCAPS) > 0:
            test_keycap_name = KEYCAPS[0].name

            args = MockArgs(names=[test_keycap_name], force=True)

            # Call make_commands
            commands = make_commands(args)

            # Check that we got commands
            self.assertGreater(
                len(commands),
                0,
                f"Should generate commands for keycap '{test_keycap_name}'",
            )

            # Check that the command contains the keycap name
            command_str = str(commands[0])
            self.assertIn(test_keycap_name, command_str)

    def test_make_commands_with_legends_flag(self):
        """Test make_commands handles the legends flag correctly"""
        # Find a keycap with actual legends
        test_keycap = None
        for keycap in KEYCAPS:
            if keycap.legends and keycap.legends != [""]:
                test_keycap = keycap
                break

        if test_keycap:
            # Temporarily modify it for this test
            original_name = test_keycap.name
            original_legends = test_keycap.legends[:]

            try:
                args = MockArgs(names=[test_keycap.name], legends=True, force=True)

                # Call make_commands
                commands = make_commands(args)

                # Should have commands for both the keycap and its legends
                self.assertGreater(
                    len(commands),
                    1,
                    "Should generate commands for both keycap and legends when legends=True",
                )

                # Check that one command is for the keycap and one is for the legends
                keycap_command = None
                legends_command = None
                for command in commands:
                    if isinstance(command, str) and "_legends" in command:
                        legends_command = command
                    elif isinstance(command, str):
                        keycap_command = command

                self.assertIsNotNone(
                    keycap_command, "Should have a command for the keycap"
                )
                self.assertIsNotNone(
                    legends_command, "Should have a command for the legends"
                )
            finally:
                # Restore original values
                test_keycap.name = original_name
                test_keycap.legends = original_legends

    def test_make_commands_with_force_flag(self):
        """Test make_commands behavior when force flag is True"""
        if len(KEYCAPS) > 0:
            test_keycap_name = KEYCAPS[0].name

            args = MockArgs(names=[test_keycap_name], force=True)

            # Call make_commands
            commands = make_commands(args)

            # With force=True, it should process the keycap regardless of file existence
            self.assertGreater(
                len(commands), 0, "Should process keycap when force=True"
            )

    @patch("os.path.exists")
    def test_make_commands_skips_existing_files_when_force_false(self, mock_exists):
        """Test that make_commands skips existing files when force flag is False"""
        mock_exists.return_value = True  # Simulate that output files exist

        if len(KEYCAPS) > 0:
            test_keycap_name = KEYCAPS[0].name

            args = MockArgs(names=[test_keycap_name], force=False)

            # Call make_commands
            commands = make_commands(args)

            # When force=False and files exist, no commands should be generated
            self.assertEqual(
                len(commands),
                0,
                "Should not generate commands when files exist and force=False",
            )

    def test_make_commands_with_empty_names_list(self):
        """Test make_commands behavior when names list is empty"""
        args = MockArgs(names=[], force=True)

        # Call make_commands
        commands = make_commands(args)

        # With empty names list, it should process all keycaps
        self.assertGreater(
            len(commands), 0, "Should process all keycaps when names list is empty"
        )

    def test_make_commands_with_nonexistent_keycap_name(self):
        """Test make_commands behavior when a specific keycap name is not found"""
        args = MockArgs(names=["nonexistent_keycap"], force=True)

        # Call make_commands
        commands = make_commands(args)

        # When keycap name is not found, no commands should be generated
        self.assertEqual(
            len(commands),
            0,
            "Should not generate commands when keycap name is not found",
        )

    def test_make_commands_with_file_type_stl(self):
        """Test make_commands generates commands with STL file type when specified"""
        # Find a keycap that exists in the KEYCAPS list
        if len(KEYCAPS) > 0:
            test_keycap_name = KEYCAPS[0].name

            args = MockArgs(names=[test_keycap_name], file_type="stl", force=True)

            # Call make_commands
            commands = make_commands(args)

            # Check that we got commands
            self.assertGreater(
                len(commands),
                0,
                f"Should generate commands for keycap '{test_keycap_name}'",
            )

            # Check that the command contains the STL file type
            command_str = str(commands[0])
            self.assertIn(test_keycap_name, command_str)
            self.assertIn(".stl", command_str)
            self.assertNotIn(".3mf", command_str)

    def test_make_commands_with_file_type_3mf(self):
        """Test make_commands generates commands with 3MF file type when specified"""
        # Find a keycap that exists in the KEYCAPS list
        if len(KEYCAPS) > 0:
            test_keycap_name = KEYCAPS[0].name

            args = MockArgs(names=[test_keycap_name], file_type="3mf", force=True)

            # Call make_commands
            commands = make_commands(args)

            # Check that we got commands
            self.assertGreater(
                len(commands),
                0,
                f"Should generate commands for keycap '{test_keycap_name}'",
            )

            # Check that the command contains the 3MF file type
            command_str = str(commands[0])
            self.assertIn(test_keycap_name, command_str)
            self.assertIn(".3mf", command_str)
            self.assertNotIn(".stl", command_str)

    def test_make_commands_default_file_type_is_stl(self):
        """Test make_commands uses STL as the default file type"""
        # Find a keycap that exists in the KEYCAPS list
        if len(KEYCAPS) > 0:
            test_keycap_name = KEYCAPS[0].name

            # Create args without specifying file_type (should default to stl)
            args = MockArgs(names=[test_keycap_name], force=True)

            # Call make_commands
            commands = make_commands(args)

            # Check that we got commands
            self.assertGreater(
                len(commands),
                0,
                f"Should generate commands for keycap '{test_keycap_name}'",
            )

            # Check that the command contains the STL file type by default
            command_str = str(commands[0])
            self.assertIn(test_keycap_name, command_str)
            self.assertIn(".stl", command_str)
            self.assertNotIn(".3mf", command_str)


if __name__ == "__main__":
    unittest.main()
