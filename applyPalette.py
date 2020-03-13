import sys
import os
import struct
import PIL.Image
from PIL import ImageChops

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

basePalette = []
with open(paletteName, "rb") as f:
    bgr = f.read(3)
    normal = ""
    while bgr:
        if sys.version_info[0] > 2:
            rgb = (bgr[2], bgr[1], bgr[0])
        else:
            rgb = (ord(bgr[2]), ord(bgr[1]), ord(bgr[0]))
        basePalette.append(rgb)
        bgr = f.read(3)
        
    

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
    
shift = [bytearray(range(0, 256))]
with open(mapName, "rb") as f:
    map = f.read(256)
    while map:
        if sys.version_info[0] > 2:
            shift.append(map)
        else:
            shift.append(bytearray(map))
        map = f.read(256)

if sys.version_info[0] > 2:
    spriteName = filedialog.askopenfilename(initialdir = "./assets",title = "Select D2 Sprite (won't be modified)",filetypes = (("d2 sprite files","*.dc6"),("all files","*.*")))
else:
    spriteName = tkFileDialog.askopenfilename(initialdir = "./assets",title = "Select D2 Sprite (won't be modified)",filetypes = (("d2 sprite files","*.dc6"),("all files","*.*")))

num = 0
newPalettes = []
colImages = []
for map in shift:
    palette = []
    row = 0
    col = 0
    fileBytes = []
    for i in map:
        fileBytes.append(basePalette[i][2])
        fileBytes.append(basePalette[i][1])
        fileBytes.append(basePalette[i][0])
        palette.append(basePalette[i])
    resDir = "./results"
    if not os.path.exists(resDir):
        os.makedirs(resDir)
    newFile = open(resDir + "/" + paletteName[0:paletteName.rfind(".")].split("/")[-1] + "_" + spriteName[0:spriteName.rfind(".")].split("/")[-1] + "-" + str(num) + ".dat", "wb")
    newFile.write(bytearray(fileBytes))
    newPalettes.append(palette)

    with open(spriteName, "rb") as f:
        spriteFile = bytearray(f.read())

    filePtr = 0
    fileSize = 4*6
    fileHeader = struct.unpack('<IIIIII', spriteFile[filePtr:filePtr + fileSize])
    filePtr += fileSize
    fileSize = 4*(fileHeader[4]*fileHeader[5])
    fmt = '<%dI' % (fileSize / 4)
    framePointers = struct.unpack(fmt, spriteFile[filePtr:filePtr + fileSize])
    filePtr += fileSize
    fileSize = 4*8
    frameHeaders = []
    for framePtr in framePointers:
        frameHeaders.append(struct.unpack('<IIIIIIII', spriteFile[framePtr:framePtr + fileSize]))
        
    print("File Header:", fileHeader)
        
    dataPtr = framePointers[0]
    index = 0
    rowImages = []
    for frameHeader in frameHeaders:
        fmt = '%dc' % frameHeader[7]
        sprite = struct.unpack(fmt, spriteFile[32 + dataPtr: 32 + dataPtr + frameHeader[7]])
                
        
        print("Sprite Offset:", dataPtr)
        print("Frame Header:", frameHeader)
        
        sys.stdout.flush()
        
        img = PIL.Image.new('RGBA', (frameHeader[1], frameHeader[2]))
        
        index1 = 0;
        index2 = 0;
        index3 = frameHeader[2] - 1;
        index4 = 0
        while index4 < frameHeader[7]:
            index4 += 1
            num1 = ord(sprite[index1]);
            index1 += 1;
            if (num1 == 128):
                index2 = 0;
                index3 -= 1;
            elif ((num1 & 128) == 128):
                index2 += (num1 & 127);
            else:
                index5 = 0
                while index5 < num1:
                    index5 += 1
                    num2 = ord(sprite[index1]);
                    index1 += 1;
                    index4 += 1;
                    img.putpixel((index2, index3), (palette[num2][0], palette[num2][1], palette[num2][2], 255))
                    index2 += 1;
        
        subDir = ""
        if(len(framePointers) > 1):
            subDir = "/" + str(index)
            if not os.path.exists(resDir + subDir):
                os.makedirs(resDir + subDir)
            
        img.save(resDir + subDir + "/" + paletteName[0:paletteName.rfind(".")].split("/")[-1] + "_" + spriteName[0:spriteName.rfind(".")].split("/")[-1] + str(num) + ".png")
        rowImages.append(img)
        
        
        dataPtr = frameHeader[6]
        index += 1
        
    row = PIL.Image.new('RGBA', (frameHeader[1] * len(framePointers), frameHeader[2]))
    i = 0
    for img in rowImages:
        row.paste(img, (i * frameHeader[1], 0))
        i += 1
    row.save(resDir + "/" + paletteName[0:paletteName.rfind(".")].split("/")[-1] + "-comp" + "_" + spriteName[0:spriteName.rfind(".")].split("/")[-1] + "-" + str(num) + ".png")
    colImages.append(row)
    num += 1
    
col = PIL.Image.new('RGBA', (frameHeader[1] * len(framePointers), frameHeader[2] * len(shift)))
i = 0
for img in colImages:
    col.paste(img, (0, frameHeader[2] * i))
    i += 1
col.save(resDir + "/" + paletteName[0:paletteName.rfind(".")].split("/")[-1] + "-comp" + "_" + spriteName[0:spriteName.rfind(".")].split("/")[-1] + ".png")
        
root.mainloop()