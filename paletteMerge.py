import sys


if sys.version_info[0] > 2:
    from tkinter import *
    from tkinter import filedialog
    root = Tk()
    filename = filedialog.askopenfilename(initialdir = "./assets",title = "Open D2 Base Palette (won't be modified)",filetypes = (("d2 palette files","*.dat"),("all files","*.*")))
else:
    from Tkinter import *
    import Tkinter, Tkconstants, tkFileDialog
    root = Tk()
    filename = tkFileDialog.askopenfilename(initialdir = "./assets",title = "Open D2 Base Palette (won't be modified)",filetypes = (("d2 palette files","*.dat"),("all files","*.*")))

MAX_ROWS = 36
FONT_SIZE = 10 # (pixels)

root.title("Palette merger by Fa-b")

bgrMap = []
with open(filename, "rb") as f:
    bgr = f.read(3)
    while bgr:
        bgrMap.append(bgr)
        bgr = f.read(3)
        
basePalette = []
for bgr in bgrMap:
    if sys.version_info[0] > 2:
        rgb = (bgr[2], bgr[1], bgr[0])
    else:
        rgb = (ord(bgr[2]), ord(bgr[1]), ord(bgr[0]))
    basePalette.append(rgb)
    

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
    
row = 0
col = 0
idx = 0

for color in basePalette:
    rgbStr = rgb_to_hex(color)
    fg = "#000000"
    if color[0] + color[1] + color[2] < 384:
        fg = "#FFFFFF"
    e = Label(root, text=str(idx) + ": " + rgbStr, background=rgbStr, font=(None, -FONT_SIZE), fg=fg)
    e.grid(row=row, column=col, sticky=E+W)
    row += 1
    if (row > 36):
        row = 0
        col += 1
    idx += 1

if sys.version_info[0] > 2:
    filename = filedialog.askopenfilename(initialdir = "./assets",title = "Select D2 Color Map (won't be modified)",filetypes = (("d2 map files","*.dat"),("all files","*.*")))
else:
    filename = tkFileDialog.askopenfilename(initialdir = "./assets",title = "Select D2 Color Map (won't be modified)",filetypes = (("d2 map files","*.dat"),("all files","*.*")))

shift = []
with open(filename, "rb") as f:
    map = f.read(256)
    while map:
        shift.append(map)
        map = f.read(256)

num = 0
newPalettes = []
for map in shift:
    palette = []
    row = 0
    col = 0
    idx = 0
    pop = Toplevel()
    pop.title("Palette " + str(num))
    for i in map:
        palette.append(basePalette[i])
        rgbStr = rgb_to_hex(basePalette[i])
        fg = "#000000"
        if color[0] + color[1] + color[2] < 384:
            fg = "#FFFFFF"
        e = Label(pop, text=str(idx) + ": " + rgbStr, background=rgbStr, font=(None, -FONT_SIZE), fg=fg)
        e.grid(row=row, column=col, sticky=E+W)
        row += 1
        if (row > 36):
            row = 0
            col += 1
        idx += 1
    newPalettes.append(palette)
    num += 1

print(shift)

sys.stdout.flush()

root.mainloop()