import numpy as np
from random import randrange
import cv2; cv = cv2;
import math
from PIL import Image, ImageFont, ImageDraw

data = [[x[0:5], x[5:8], x[8:10], x[10:]] for x in open('CWFS64W3.HF.TXT','r').read().split('\n') if len(x)];

font = ImageFont.truetype("cwTeXFangSong-zhonly.ttf",256)

def rastBox(l):
  im0 = Image.new("L",(256,256))
  dr0 = ImageDraw.Draw(im0)
  dr0.text((10,1),l,255,font=font)
  im = np.array(im0)
  ret,th = cv2.threshold(im,128,255,cv2.THRESH_BINARY);
  return th;

for i in range(0,len(data)):
  pd = data[i][3];
  ps = [[]]
  for j in range(0,len(pd),2):
    if pd[j:j+2] == ' R':
      ps.append([])
      continue;
    x = ord(pd[j])-ord('R')
    y = ord(pd[j+1])-ord('R')
    if ((not len(ps[-1])) or (ps[-1][-1][0] != x or ps[-1][-1][1] != y)):
      ps[-1].append([x,y])
  
  ps = [np.array([list(y) for y in x],np.int32).reshape(-1,1,2) for x in ps]
  ps = [(p*4).astype(np.int32)+np.array([128,128]) for p in ps]
  # ps = [(p*4).astype(np.int32)+np.array([128+random.randrange(-10,10),128+random.randrange(-10,10)]) for p in ps]
  
  im = np.zeros((256,256),np.uint8);
  cv.polylines(im, ps, False, 255, 1)

  b = rastBox(chr(int(data[i][0]))).astype(np.float32)

  # im = im.astype(np.float32)/255.0 * 0.5 + b/255.0 * 0.5;

  im = np.hstack((im,b));

  im = np.dstack((im,im,im))

  # cv2.imshow('',im);cv2.waitKey(0)

  cv2.imwrite("warped/"+str(i).zfill(4)+".png",im);
