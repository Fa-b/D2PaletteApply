import sys


if sys.version_info >= (2, 7):
    from tkinter import *
    from tkinter import filedialog
    root = Tk()
    filename = filedialog.askopenfilename(initialdir = "./",title = "Open D2 Base Palette (won't be modified)",filetypes = (("d2 palette files","*.dat"),("all files","*.*")))
else:
    from Tkinter import *
    import Tkinter, Tkconstants, tkFileDialog
    root = Tk()
    filename = tkFileDialog.askopenfilename(initialdir = "./",title = "Open D2 Base Palette (won't be modified)",filetypes = (("d2 palette files","*.dat"),("all files","*.*")))

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
    if sys.version_info >= (2, 7):
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
    e = Label(root, text=str(idx) + ": " + rgbStr, background=rgbStr, font=(None, -FONT_SIZE))
    e.grid(row=row, column=col, sticky=E+W)
    row += 1
    if (row > 36):
        row = 0
        col += 1
    idx += 1

sys.stdout.flush()

root.mainloop()