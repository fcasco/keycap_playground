# Keycap Playground

## Overview

The Keycap Playground is a parametric OpenSCAD keycap generator
that allows you to create keycaps of various shapes, sizes, and profiles.
This repository contains modules for generating keycaps, stems, legends, and utility functions.

## File Structure

- `keycap_playground.scad` - Main entry point with global parameters and rendering logic
- `keycaps.scad` - Core keycap generation modules
- `stems.scad` - Stem generation modules for various switch types
- `legends.scad` - Legend (text/symbol) generation
- `profiles.scad` - Predefined keycap profiles (DSA, DCS, KAT, Riskeycap, etc.)
- `utils.scad` - Utility functions and geometric primitives
- `snap_fit.scad` - Snap-fit stem modules
- `src/` - Python scripts for command-line keycap generation

## Key Concepts

### 1. Global Parameters System
- Use the global variables in `keycap_playground.scad` to configure your keycap
- Parameters like `KEY_PROFILE`, `KEY_HEIGHT`, `WALL_THICKNESS`, etc. control the keycap properties
- Profiles (e.g. "riskeycap", "dsa", "dcs") override many specific parameters

### 2. Rendering Modes
- `RENDER` variable controls what gets generated: `["keycap"]`, `["stem"]`, `["legends"]`, or combinations
- For multi-material printing: render keycap, stem, and legends separately
- Use `VISUALIZE_LEGENDS = true` to improve preview performance when working with legends

### 3. Keycap Profiles
- Standard profiles: "dsa", "dcs", "dss", "kat", "kam", "riskeycap", "gem", "xda"
- Custom profile: use empty `KEY_PROFILE = ""` to use custom parameters
- Each profile has specific dimensions and characteristics optimized for mechanical keyboard standards

## Best Practices

### Performance Optimization
- Use `$fn = 32` for preview, higher values (64-256) for final render
- Set `VISUALIZE_LEGENDS = true` when positioning legends to improve preview speed
- Use `DISH_FN` and `DISH_CORNER_FN` appropriately - lower values for preview, higher for final render
- For complex designs, consider using `--enable=fast-csg` flag with newer OpenSCAD versions

### 3D Printing Considerations
- **Print Orientation**: For smooth tops, print keycaps on their side using `KEY_ROTATION`
  - Example for Riskeycap: `KEY_ROTATION = [0,110.1,90]`
- **Side Supports**: When printing on side, use `STEM_SIDE_SUPPORTS = [0,1,0,0]` to add internal supports
- **Wall Thickness**: Use `WALL_THICKNESS = 1.2` (3x 0.4mm nozzle width) as minimum for durability
- **Dish Thickness**: Minimum `DISH_THICKNESS = 1.0` for good legend printing
- **Infill**: No internal infill needed due to hollow design

### Design Guidelines

#### Parameter Relationships
```openscad
// Key dimensions
KEY_UNIT = 19.05;                       // Standard keyboard unit
BETWEENSPACE = 0.8;                     // Gap between keycaps
KEY_LENGTH = (KEY_UNIT*1-BETWEENSPACE); // Standard 1U key
KEY_WIDTH = (KEY_UNIT*1-BETWEENSPACE);  // Standard 1U key

// Wall and dish relationships
WALL_THICKNESS = 0.45*2.25;             // ~1mm wall
DISH_THICKNESS = 1.0;                   // At least 1mm for legend strength
UNIFORM_WALL_THICKNESS = true;          // For consistent wall thickness matching dish
```

#### Dish Configuration
- `DISH_TYPE`: "sphere", "cylinder", "inv_pyramid", or "" (flat)
- `DISH_DEPTH`: How deep the dish cuts into the keycap
- `DISH_THICKNESS`: Material thickness at dish bottom
- `DISH_FN`: Resolution of dish curves (higher = smoother but slower)

#### Legend Positioning
- Use `LEGEND_TRANS` for simple position adjustments
- Use `LEGEND_ROTATION` and `LEGEND_TRANS2` for complex positioning
- Start with single legend, verify positioning before adding more
- Use `LEGEND_FONTS` with fonts that have good character support (Noto, Code2000)

### Advanced Features

#### Multi-Material Printing
```openscad
// Render separately for multi-material
// 1. Render ["keycap", "stem"] for base material
// 2. Render ["legends"] for accent color
```

#### Uniform Wall Thickness
- `UNIFORM_WALL_THICKNESS = true` creates consistent wall thickness that matches dish shape
- Better for injection molding and consistent strength
- More computationally intensive to render

#### Snap-Fit Stems
- `STEM_SNAP_FIT = true` creates removable stems
- Use with `STEM_SIDES_WALL_THICKNESS` for legend support

#### Homing Dots
```openscad
HOMING_DOT_LENGTH = 3;  // Width of dot
HOMING_DOT_WIDTH = 1;   // Depth of dot
HOMING_DOT_Y = -KEY_WIDTH/4; // Position at front of key
HOMING_DOT_Z = -0.35;   // Depth (negative = below surface)
```

## Common Workflows

### 1. Creating a Simple Keycap
1. Set `KEY_PROFILE` to desired profile or leave empty for custom
2. Adjust dimensions like `KEY_HEIGHT`, `WALL_THICKNESS`
3. Set `LEGENDS` array with desired characters
4. Set `RENDER = ["keycap", "stem"]`
5. Render with F6

### 2. Multi-Material Legend Keycap
1. Configure keycap parameters
2. Position legends with `LEGEND_TRANS`, `LEGEND_ROTATION`
3. Render with `RENDER = ["keycap", "stem"]`
4. Render separately with `RENDER = ["legends"]`
5. Use different colors for each STL in your slicer

### 3. Custom Profile Development
1. Create new module in profiles.scad following existing patterns
2. Define dimensional arrays based on reference measurements
3. Test with `KEY_PROFILE = "yourprofile"` in keycap_playground.scad

### 4. Batch Key Generation
- Use `ROW` variable with `RENDER = ["row"]`, `["row_stems"]`, `["row_legends"]`
- Command line: `openscad -o output.stl -D "ROW='[[\"Q\"],[\"W\"],[\"E\"]]'" keycap_playground.scad`

### 5. Command Line and Script-Based Generation
- Use Python scripts in `scripts/` directory for automated batch generation
- The `Keycap` class in `keycap.py` generates OpenSCAD command lines based on parameters
- For automated generation of complete keyboard sets, use specialized scripts like `riskeycap_full.py`
- Use `--legends` flag to generate separate legend files for multi-material printing
- Use `--force` flag to regenerate files that already exist

## Debugging Tips

- Use `DEBUG = true` to output parameter values to console
- Use `%` modifier to visualize legends positionally during development
- Use `F5` for fast preview, `F6` for final render
- For complex legends, verify with `VISUALIZE_LEGENDS = true`
- Check that `STEM_OUTSIDE_TOLERANCE` values accommodate your printer's accuracy

## File Modifications

### Adding New Profiles
To add a new profile:
1. Add keycap module to `profiles.scad` following the naming convention `PROFILENAME_keycap`
2. Add corresponding stem module `PROFILENAME_stem`
3. Update `handle_render()` in `keycap_playground.scad` to recognize the new profile

### Custom Geometries
- Use `rpoly()` for polygonal key shapes
- Use `squarish_rpoly()` for trapezoidal extrusions
- Use `polygon_layers`, `polygon_layer_rotation`, `polygon_curve` for complex topographies

## Performance Optimization

- For previews: Use low `$fn`, `VISUALIZE_LEGENDS = true`
- For complex shapes: Consider using `POLYGON_LAYERS` with lower values
- For final renders: Use appropriate `$fn` values (64-256) based on complexity and desired quality

## File Organization

When creating custom designs:
- Keep parameter modifications in separate .scad files that `use` the main modules
- Use descriptive variable names for custom configurations
- Comment changes explaining the reasoning for future reference
- Consider using `include` instead of `use` if you need to modify constants rather than modules

## Python Script Automation

The `scripts/` directory contains Python automation tools for batch generating keycaps:

### Keycap Class
- The `keycap.py` file defines the `Keycap` class which provides an abstraction for generating OpenSCAD command lines
- This class encapsulates all the parameters needed to generate a keycap and can output the exact OpenSCAD command needed
- Supports both regular rendering and multi-material rendering via colorscad.sh

### Specialized Keycap Classes
- Scripts like `riskeycap_full.py` and `gem_full.py` define specialized subclasses for different keycap variations
- Each subclass inherits from a base class and adjusts specific parameters like:
  - Font sizes and positions for different legends
  - Key rotation for different profiles (e.g., `[0,110.1,90]` for Riskeycap profile printed on side)
  - Dimensions for different key sizes (1U, 1.25U, 1.5U, 2U, etc.)
  - Special handling for specific characters (e.g., different fonts for @ symbol in riskeycap_2)

### Batch Generation Scripts
- `riskeycap_full.py`: Generates a complete set of Riskeycap profile keycaps with Gotham Rounded font
- `gem_full.py`: Generates GEM profile keycaps 
- `riskeyboard_70.py`: Generates keycaps for a specific 70% keyboard layout
- These scripts use the `KEYCAPS` list to define all possible keycaps to generate

### Command Line Usage

**Important**: Before using the scripts, ensure OpenSCAD is installed and accessible in your PATH
(`which openscad` should return a path).

```sh
# Show help
python -m src --help

# Show all available keycap names
python -m src --keycaps

# Generate specific keycaps to output directory
python -m src --out /tmp/keycaps A B C

# Generate all keycaps to output directory (warning: this will take a very long time)
python -m src --out /tmp/keycaps

# Force regeneration even if files exist
python -m src --out /tmp/keycaps --force A B C

# Generate separate legend files for multi-material printing
python -m src --out /tmp/keycaps --legends A B C
```

### Custom Keycap Generation
To create your own keycap set:
1. Define a base class inheriting from `Keycap` with your preferred parameters
2. Create specialized subclasses for different legend layouts (alphas, numbers, symbols)
3. Add your keycaps to a `KEYCAPS` list
4. Use the command-line interface to generate STLs

### Asynchronous Processing
The  script includes asyncio functionality to run multiple OpenSCAD processes in parallel for faster batch generation.

### Legend Positioning via Scripts
- Use `trans` parameter for legend translation: `[x, y, z]`
- Use `rotation` parameter for legend rotation: `[x, y, z]` in degrees
- Use `scale` parameter to adjust legend dimensions: `[x, y, z]`
- The `postinit()` method allows override of any parameter via kwargs
