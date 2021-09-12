import numpy as np
from random import randrange
import cv2; cv = cv2;
import math

data = [[x[0:5], x[5:8], x[8:10], x[10:]] for x in open('CWFS64J.HF.TXT','r').read().split('\n') if len(x)];

oo = '<html>'


do_sobel = True;

mk = 99999999
Mk = 0
ak = 0

asdy = 0
asy = 0

# 22.3766 104.09130288294601 128.2776
# 622.04956 3970.1596921884493 7611.0947

def mapval(value,istart,istop,ostart,ostop):
    return ostart + (ostop - ostart) * ((value - istart)*1.0 / (istop - istart))

def clampmap(value,istart,istop,ostart,ostop):
  if (ostart < ostop):
    return min(max(mapval(value,istart,istop,ostart,ostop),ostart),ostop);
  else:
    return max(min(mapval(value,istart,istop,ostart,ostop),ostart),ostop);
  

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
      ps[-1].append([(x)/64,(y)/64])
  
  sdy = 0.12
  sy = 1

  if do_sobel:
    im = cv2.imread("data_all/"+str(i).zfill(4)+".png",0)[:,256:];

    im = cv.GaussianBlur(im, (11, 11), 0)
    gy = np.abs(cv.Sobel(im, cv.CV_16S, 0, 1, ksize=5, scale=1, delta=0, borderType=cv.BORDER_DEFAULT).astype(np.float32))*0.0001
    # print(np.max(gy),np.min(gy))
    # cv2.imshow("",gy);cv2.waitKey(0)
    # continue;

    k = np.sum(np.amax(gy, 1))
    # print(k)
    # continue;
    # k = np.sum(gy);
    # mk = min(k,mk)
    # Mk = max(k,Mk)
    # ak += k/len(data);
    # continue;

    sdy = clampmap(k,100,120,0.12,0.06)
    sy = clampmap(k,30,120,0.75,1.05);
    # asdy += sdy;
    # asy += sy;
    # continue;

  for p in ps:
    for j in range(0,len(p)):
      x,y = p[j]

      dy = max(0,math.cos(y*math.pi*1.0))*sdy-0.02


      x = x * ((y+0.5)*0.22+0.9)
      y += dy
      y = y * 0.85 + 0.00

      x*=0.8
      y*=0.8

      y -= math.cos(x*math.pi)*0.03*((y+0.5))
      y -= x*0.05

      y *= sy

      p[j] = [x,y]
  # print(p[j])
  o = '2r';
  f = True;
  for p in ps:
    if not f:
      o += ' R';
    else:
      f = False
    for q in p:
      o += chr(ord('R')+int(round(q[0]*64)))
      o += chr(ord('R')+int(round(q[1]*64)))

  o = str(data[i][0]) + str(len(o)//2).rjust(3) + o;
  print(o)


# print(mk,ak,Mk)
# print(asdy/len(data),asy/len(data));
