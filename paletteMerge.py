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
        
if sys.version_info[0] > 2:
    spriteName = filedialog.askopenfilename(initialdir = "./assets",title = "Select D2 Sprite (won't be modified)",filetypes = (("d2 sprite files","*.dc6"),("all files","*.*")))
else:
    spriteName = tkFileDialog.askopenfilename(initialdir = "./assets",title = "Select D2 Sprite (won't be modified)",filetypes = (("d2 sprite files","*.dc6"),("all files","*.*")))

num = 0
newPalettes = []
images = []
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
    newFile = open(resDir + "/" + paletteName[0:paletteName.rfind(".")].split("/")[-1] + "_" + spriteName[0:spriteName.rfind(".")].split("/")[-1] + str(num) + ".dat", "wb")
    newFile.write(bytearray(fileBytes))
    newPalettes.append(palette)
    num += 1

    fileHeader = []
    framePointers = []
    frameHeader = []
    sprite = []
    with open(spriteName, "rb") as f:
        long = f.read(4)
        while len(fileHeader) < 6:
            fileHeader.append(struct.unpack('<i', long)[0])
            long = f.read(4)
        while len(framePointers) < (fileHeader[4] * fileHeader[5]):
            framePointers.append(struct.unpack('<i', long)[0])
            long = f.read(4)
        if(len(framePointers) > 1):
            raise ValueError('Not supporting multiple frames & directions yet :-(.')
        # TODO read file into bytearray and work with that, that way we can jump to the adress offset of each frame_header
        while len(frameHeader) < 7:
            frameHeader.append(struct.unpack('<i', long)[0])
            long = f.read(4)
        frameHeader.append(struct.unpack('<i', long)[0])
        data = f.read(1)
        while data:
            sprite.append(ord(struct.unpack('c', data)[0]))
            data = f.read(1)
            
    # sprite.reverse()
        
    print("File Header:", fileHeader)
    print("Frame Header:", frameHeader)
    print("Sprite:", len(sprite))
    sys.stdout.flush()
    
    # print(len(sprite))
        
    # pic = []
    # x = 0
    # y = 0
    # pic.append([]);
    # for idx in range(0, frameHeader[7]):
        # code = sprite[idx]
        # if (code == 128):
            # pic[y].append([255,255,255])
            # x = 0
            # y += 1
            # pic.append([]);
            # continue
        # elif (code & 128) == 128:
            # for j in range(0, code & 128):
                # pic[y].append([255,255,255])
        # else:
            # pic[y].append(palette[code])
        # x += 1
        
    # img = PIL.Image.new('RGBA', (frameHeader[1], frameHeader[2]))
    
    # print("x:", len(pic[0]))
    # print("y:", len(pic))
    # sys.stdout.flush()
    
    # for x in range(0, len(pic[0])):
        # for y in range(len(pic)):
            # if pic[x][y] == [255,255,255]:
                # img.putpixel((x,y), (0,0,0,0))
            # else:
                # img.putpixel((x, y), (pic[x][y][0], pic[x][y][1], pic[x][y][2], 255))
       
    
    img = PIL.Image.new('RGBA', (frameHeader[1], frameHeader[2]))
    
    index1 = 0;
    index2 = 0;
    index3 = frameHeader[2] - 1;
    index4 = 0
    while index4 < frameHeader[7]: #for(long index4 = 0; index4 < (long) dc6FrameHeader.length; ++index4)
        index4 += 1
        num1 = sprite[index1];
        index1 += 1;
        if (num1 == 128):
            index2 = 0;
            index3 -= 1;
        elif ((num1 & 128) == 128):
            index2 += (num1 & 127);
        else:
            index5 = 0
            while index5 < num1: #for(long index5 = 0; index5 < (long) num1; ++index5)
                index5 += 1
                num2 = sprite[index1];
                index1 += 1;
                index4 += 1;
                img.putpixel((index2, index3), (palette[num2][0], palette[num2][1], palette[num2][2], 255))
                index2 += 1;

    images.append(img)
    img.save(resDir + "/" + paletteName[0:paletteName.rfind(".")].split("/")[-1] + "_" + spriteName[0:spriteName.rfind(".")].split("/")[-1] + str(num) + ".png")
    
compilation = PIL.Image.new('RGBA', (frameHeader[1] * len(shift), frameHeader[2]))
i = 0
for img in images:
    i += 1
    compilation.paste(img, (i * frameHeader[1], 0))
compilation.save(resDir + "/" + paletteName[0:paletteName.rfind(".")].split("/")[-1] + "-comp" + "_" + spriteName[0:spriteName.rfind(".")].split("/")[-1] + str(num) + ".png")
    
root.mainloop()