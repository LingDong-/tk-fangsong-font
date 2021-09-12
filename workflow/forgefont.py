from glob import glob
import os
import sys
import json
import fontforge

name = "tkFangSong"

font = fontforge.font()
font.familyname = name
font.fontname = name
font.fullname= name
font.copyright = "Copyright (c) 2021, Lingdong Huang"
font.version = "0.0.1"

simp = json.loads(open("TC2SC.json",'r').read())
simp = [[x,simp[x]] for x in simp]

files = glob("fine/*.svg");


sf = set([x[-5] for x in files])

for f in files:
    hx = int(os.path.basename(f)[0:5])

    glyph = font.createChar(hx)
    glyph.importOutlines(f)
    glyph.width=800
    # glyph.simplify()

    other = set()
    for o in simp:
        if o[0] == chr(hx):
            other.add(o[1])
        elif o[1] == chr(hx):
            other.add(o[0])
            
    other = other - sf
    # print(f,other)
    if len(other) > 0:
        glyph.altuni = [ ord(o) for o in other ]


glyph = font.createChar(0x3000)
glyph.width=800
glyph = font.createChar(0x20)
glyph.width=800

print(len(list(font.glyphs())))

font.generate("dist/"+name+".ttf")

os.system("python3 fixfont.py dist/"+name+".ttf")








