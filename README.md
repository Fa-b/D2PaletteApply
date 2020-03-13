# D2PaletteApply
<p>A little python tool to generate palette items</p>
<p>This script was only implemented to generate colored item images and font images once for this project here:<br>
  https://github.com/Fa-b/ItemScreenshot<br><br>
Maybe it can still be of use to someone.</p>

# Requirements
- Installed python (tested only v3.8 atm)
- Installed PIL

# Usage
start from shell using `python applyPalette`
- first select a palette, for example pal.dat (./assets/)
- select a colormap, for example invgreybrown.dat (./assets/)
- select a .dc6 item file

<p>All will be applied and output saved to `./results/`.<br>
.dc6 files containing multiple frames and or directions are also supported now.<br>
We have generated a new colormap for font colors. You can find it in the `/assets/font_shift.dat`</p>

Have fun :-)


# Outputs
- All colored items as `.png`
- All generated .dat color palettes from mapping.
