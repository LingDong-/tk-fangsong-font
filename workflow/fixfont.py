from glob import glob
import os
import sys
import json
import fontforge

font = fontforge.open(sys.argv[1])
font.hasvmetrics = 1
font.generate(sys.argv[1])
