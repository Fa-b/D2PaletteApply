import sys
import os
import struct

if sys.version_info[0] > 2:
    from tkinter import *
    from tkinter import filedialog
    root = Tk()
    paletteName = filedialog.askopenfilename(initialdir = "./assets",title = "Open D2 Base Palette (won't be modified)",filetypes = (("d2 palette files","*.dat"),("all files","*.*")))
else:
    from Tkinter import *
    import Tkinter, Tkconstants, tkFileDialog
    root = Tk()
    paletteName = tkFileDialog.askopenfilename(initialdir = "./assets",title = "Open D2 Base Palette (won't be modified)",filetypes = (("d2 palette files","*.dat"),("all files","*.*")))

MAX_ROWS = 36
FONT_SIZE = 10 # (pixels)

root.title("Palette merger by Fa-b")

bgrMap = []
with open(paletteName, "rb") as f:
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
    mapName = filedialog.askopenfilename(initialdir = "./assets",title = "Select D2 Color Map (won't be modified)",filetypes = (("d2 map files","*.dat"),("all files","*.*")))
else:
    mapName = tkFileDialog.askopenfilename(initialdir = "./assets",title = "Select D2 Color Map (won't be modified)",filetypes = (("d2 map files","*.dat"),("all files","*.*")))

shift = []
with open(mapName, "rb") as f:
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
    #idx = 0
    #pop = Toplevel()
    #pop.title("Palette " + str(num))
    fileBytes = []
    for i in map:
        fileBytes.append(basePalette[i][2])
        fileBytes.append(basePalette[i][1])
        fileBytes.append(basePalette[i][0])
        palette.append(basePalette[i])
        #rgbStr = rgb_to_hex(basePalette[i])
        #fg = "#000000"
        #if color[0] + color[1] + color[2] < 384:
        #    fg = "#FFFFFF"
        #e = Label(pop, text=str(idx) + ": " + rgbStr, background=rgbStr, font=(None, -FONT_SIZE), fg=fg)
        #e.grid(row=row, column=col, sticky=E+W)
        #row += 1
        #if (row > 28):
        #    row = 0
        #    col += 1
        #idx += 1
    resDir = "./results"
    if not os.path.exists(resDir):
        os.makedirs(resDir)
    newFile = open(resDir + "/" + paletteName[0:paletteName.rfind(".")].split("/")[-1] + "_" + str(num) + ".dat", "wb")
    newFile.write(bytearray(fileBytes))
    newPalettes.append(palette)
    num += 1
    
if sys.version_info[0] > 2:
    spriteName = filedialog.askopenfilename(initialdir = "./assets",title = "Select D2 Sprite (won't be modified)",filetypes = (("d2 sprite files","*.dc6"),("all files","*.*")))
else:
    spriteName = tkFileDialog.askopenfilename(initialdir = "./assets",title = "Select D2 Sprite (won't be modified)",filetypes = (("d2 sprite files","*.dc6"),("all files","*.*")))

fileHeader = []
framePointers = []
frameHeader = []
sprite = []
with open(spriteName, "rb") as f:
    long = struct.unpack('<i', f.read(4))[0]
    while len(fileHeader) < 6:
        fileHeader.append(long)
        long = struct.unpack('<i', f.read(4))[0]
    while len(framePointers) < (fileHeader[4] * fileHeader[5]):
        framePointers.append(long)
        long = struct.unpack('<i', f.read(4))[0]
    if(len(framePointers) > 1):
        raise ValueError('Not supporting multiple frames & directions yet :-(.')
    # TODO read file into bytearray and work with that, that way we can jump to the adress offset of each frame_header
    while len(frameHeader) < 8:
        frameHeader.append(long)
        long = struct.unpack('<i', f.read(4))[0]
        
print("File Header:", fileHeader)
print("Frame Header:", frameHeader)

sys.stdout.flush()

root.mainloop()