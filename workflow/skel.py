import numpy as np
import cv2; cv = cv2;
import trace_skeleton;
from PIL import Image, ImageFont, ImageDraw

CH0 = 0x4e00 # unicode <CJK Ideograph, First>
CH1 = 0x9fff # unicode <CJK Ideograph, Last>

font = ImageFont.truetype("cwTeXFangSong-zhonly.ttf",640)

# create a matrix containing raster image of character
def rastBox(l):
  im0 = Image.new("L",(640,640))
  dr0 = ImageDraw.Draw(im0)
  dr0.text((25,5),l,255,font=font)
  
  im = np.array(im0)

  ret,th = cv2.threshold(im,200,255,cv2.THRESH_BINARY);
  # th = cv2.erode(th,np.array([[1,1,1],[1,1,1],[1,1,1]],np.uint8),iterations=2);
  return th;

no = rastBox(chr(0x4e02)).astype(np.float32);

for i in range(CH0,CH1+1):
  # print(chr(i))
  im = rastBox(chr(i));

  if abs(np.sum(im.astype(np.float32) - no)) < 1000:
    continue

  # cv2.imshow('',im);cv2.waitKey(0);

  # contours, hierarchy = cv.findContours(im, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

  # contours = [cv2.approxPolyDP(c,0.2,True)//2 for c in contours]

  # vis = np.zeros((512,512),np.uint8);
  # cv.drawContours(vis, [c*5 for c in contours], -1, 255, 1)
  # cv2.imshow('',vis);cv2.waitKey(0);

  ps = trace_skeleton.from_numpy(im);
  ps = [np.array([list(y) for y in x],np.int32).reshape(-1,1,2) for x in ps]
  ps = [cv2.approxPolyDP(c,6,False) for c in ps]

  ps = [np.round(p/5).astype(np.int32)//2 for p in ps]

  # cv.polylines(vis, [p*8 for p in ps], False, 255, 1)
  # cv.polylines(vis, [p+np.array([1,0]) for p in ps], False, 255, 1)
  # cv2.imshow('',vis);cv2.waitKey(0);
  # print(ps);

  o = '2r';
  f = True;
  for p in ps:
    if not f:
      o += ' R';
    else:
      f = False
    for q in p:
      o += chr(ord('R')+(q[0,0]-32))
      o += chr(ord('R')+(q[0,1]-32))

  o = str(i).rjust(5) + str(len(o)//2).rjust(3) + o;
  print(o)
