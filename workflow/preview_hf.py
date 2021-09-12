import numpy as np
from random import randrange
import cv2; cv = cv2;
import math

np.seterr(all='raise')

data0 = [[x[0:5], x[5:8], x[8:10], x[10:]] for x in open('CWFS64J.HF.TXT','r').read().split('\n') if len(x)];
data1 = [[x[0:5], x[5:8], x[8:10], x[10:]] for x in open('CWFS64W3.HF.TXT','r').read().split('\n') if len(x)];
oo = '<html>'

def getps(pd):
  ps = [[]]
  for j in range(0,len(pd),2):
    if pd[j:j+2] == ' R':
      ps.append([])
      continue;
    x = ord(pd[j])-ord('R')
    y = ord(pd[j+1])-ord('R')
    if ((not len(ps[-1])) or (ps[-1][-1][0] != x or ps[-1][-1][1] != y)):
      ps[-1].append([x,y])

  return ps
for i in range(0,len(data1)):
  # ps0 = getps(data0[i][3])
  ps1 = getps(data1[i][3])

  o = f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" style="border:1px solid black">'
  # o += f'<text x="10" y="10" font-size="10">{chr(int(data0[i][0]))}</text>'
  # o += f'<path fill="none" stroke="silver" d="'
  # for p in ps0:
  #   o += " M "
  #   for q in p:
  #     o += f'{q[0]+32} {q[1]+32} '
  # o += f'" />'

  o += f'<path fill="none" stroke="black" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" d="'
  for p in ps1:
    o += " M "
    for q in p:
      o += f'{q[0]+32} {q[1]+32} '
  o += f'" />'
  o += '</svg>'

  oo += o
oo += '</html>'
print(oo)