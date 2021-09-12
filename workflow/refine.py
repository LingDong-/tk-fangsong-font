from glob import glob
import cv2; cv = cv2;
import numpy as np
import math
from perlin import perlin_img


INP1 = "images/*-outputs.png";
INP2 = "retouched/*-outputs.png";
OUTP = "fine";

def img_id(x):
  return int(x.split('/')[-1].split('-')[0])

files = sorted(glob(INP1),key=img_id)
filesr = sorted(glob(INP2),key=img_id)

for i in range(len(files)):
  for j in range(len(filesr)):
    if img_id(files[i]) == img_id(filesr[j]):
      files[i] = filesr[j]

# print(files)

data = [[x[0:5], x[5:8], x[8:10], x[10:]] for x in open('CWFS64W.HF.TXT','r').read().split('\n') if len(x)];

# print(len(data)==len(files))


mdx = 20
mdy = 5
for i in range(len(files)):
  im = cv2.imread(files[i]);
  im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY);

  im = im.astype(np.float32)
  rand = np.random.random(im.shape)*0.3+0.7
  rand1 = perlin_img(im.shape[0],20)
  rand2 = perlin_img(im.shape[0],100)
  rand = rand2*0.4+0.4*rand1+0.2


  im *= rand
  im = im.astype(np.uint8)
  # cv2.imshow('',im);cv2.waitKey(0)

  im = cv2.adaptiveThreshold(255-im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,29,1)


  # _, im = cv2.threshold(im,127,255,0);

  im = 255-im;

  im[:,-8:] = 0
  im[:,:8] = 0
  im[-8:,:] = 0
  im[:8,:] = 0

  # cv2.imshow('',im);cv2.waitKey(0)
  # continue;


  im2 = np.zeros((300,300),np.uint8);

  M = cv2.moments(im);
  cx = int(M['m10']/M['m00'])
  cy = int(M['m01']/M['m00'])

  dx = 128 - cx
  dy = 128 - cy
  # print(dx,dy)
  if dx < 0:
    dx = max(dx,-mdx)
  else:
    dx = min(dx,mdx)
  if dy < 0:
    dy = max(dy,-mdy)
  else:
    dy = min(dy,mdy)

  im2[22+dy:22+256+dy,22+dx:22+256+dx] = im;
  im2 = im2[22:22+256,22:22+256]


  im2 = cv2.resize(im2,(512,512),interpolation=cv2.INTER_LANCZOS4)
  im2 = cv.GaussianBlur(im2,(9,9),0);
  _, im2= cv2.threshold(im2,127,255,0);


  im2 = 255-im2
  cv2.imwrite(OUTP+'/'+data[i][0]+chr(int(data[i][0]))+".png",im2);

