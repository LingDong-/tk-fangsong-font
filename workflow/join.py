import numpy as np
from random import randrange
import cv2; cv = cv2;
import math

np.seterr(all='raise')

data = [[x[0:5], x[5:8], x[8:10], x[10:]] for x in open('CWFS64.HF.TXT','r').read().split('\n')];

def ang_between(v1,v2):
  try:
    u1 = v1 / np.linalg.norm(v1)
    u2 = v2 / np.linalg.norm(v2)
    dp = np.dot(u1, u2)
    return np.arccos(dp)
  except:
    return 9999

def are_close(v1,v2):
  return abs(v1[0]-v2[0]) <= 2 and abs(v1[1]-v2[1]) <= 3

def to_cv(ps):
  return [x.astype(np.int32).reshape(-1,1,2) for x in ps]

def disp(ps):
  vis = np.zeros((512,512,3),np.uint8);
  qs = to_cv(ps)
  for i,p in enumerate(qs):
    c = (randrange(255),randrange(255),randrange(255))
    cv.polylines(vis, [p*8+256], False, c, 3)
    cv.putText(vis,str(i),tuple(p[0,0]*8+256),cv.FONT_HERSHEY_SIMPLEX,2,c,1,8)
  cv2.imshow('',vis);cv2.waitKey(0);


def proc(ps):
  dbg = False
  da = 30 * math.pi/180

  if dbg: print('-------')

  for j in range(len(ps)):
    for k in range(len(ps)):
      if j == k : continue
      if dbg:  print(j,k)

      if are_close(ps[j][-1],ps[k][0]):
        if dbg:  print('?1')
        ang = ang_between(ps[j][-1]-ps[j][-2], ps[k][1]-ps[k][0])
        if dbg: print(ang*180/math.pi)
        if (ang < da):
          if dbg:  print('a',j,k)
          ps[j] = np.vstack((ps[j],ps[k][1:]))
          ps.pop(k)
          return proc(ps)

      if are_close(ps[j][-1],ps[k][-1]):
        if dbg:  print('?2')

        ang = ang_between(ps[j][-1]-ps[j][-2], ps[k][-2]-ps[k][-1])
        if dbg: print(ang*180/math.pi)
        if ang < da:
          if dbg:  print('b',j,k)
          ps[j] = np.vstack((ps[j],np.flip(ps[k],axis=0)[1:]))

          ps.pop(k)
          return proc(ps)

      if are_close(ps[j][0],ps[k][0]):
        if dbg:  print('?3')

        ang = ang_between(ps[j][0]-ps[j][1],ps[k][1]-ps[k][0])
        if dbg: print(ang*180/math.pi)
        if ang < da:
          if dbg:  print('c',j,k)
          ps[j] = np.vstack((np.flip(ps[j],axis=0),ps[k][1:]))
          ps.pop(k)
          return proc(ps)

      if dbg:  print('...')
  return ps



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
  
  ps = [x for x in ps if len(x)>=2]
  # print(i,ps)
  ps = [np.array(x,np.float32) for x in ps]
  
  # disp(ps)

  ps = proc(ps)

  # disp(ps)

  # exit()

  ps = to_cv(ps)

  o = '2r';
  f = True;
  for p in ps:
    if not f:
      o += ' R';
    else:
      f = False
    for q in p:

      o += chr(ord('R')+(q[0,0]))
      o += chr(ord('R')+(q[0,1]))

  # o = str(i).rjust(5) + str(len(o)//2).rjust(3) + o;
  o = data[i][0] + str(len(o)//2).rjust(3) + o;
  # print(len(''.join(data[i]))-len(o))
  print(o)
  # exit()