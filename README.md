# D2PaletteApply
<p>A little python tool to generate palette items</p>
<p>This script was only implemented to generate colored item images once for [this](https://github.com/Fa-b/ItemScreenshot)Project.<br>
Maybe it can still be of use to someone.</p>

# Requirements
- Installed python (tested v2.7 & v3.8)
- Installed PIL

# Usage
start from shell using `python applyPalette`
- first select a palette, for example pal.dat (./assets/)
- select a colormap, for example invgreybrown.dat (./assets/)
- select a .dc6 item file

<p>All will be applied and output saved to `./results/`.<br>
only .dc6 files containing single frames and directions are possible at the moment.<br>
Changing the implementation to support more files will be easy though.</p>


# Outputs
- All colored items as `.png`
- All generated .dat color palettes from mapping.
