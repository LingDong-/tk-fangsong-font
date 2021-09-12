import cv2
import sys
from glob import glob
import os

# print(sys.argv)

g = sys.argv[1]
files = glob(g);

g2 = g.replace('.png','.bmp');

print(g)
print(g2)


for f in files:
	im = cv2.imread(f);
	cv2.imwrite(f.replace('.png','.bmp'),im);

print(1)

os.system(f"potrace --svg {g2}")

print(2)

os.system(f'rm -rf {g2}')

print(3)