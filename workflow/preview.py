from glob import glob
import os;

o = '<html><body style="background:#222;filter:invert(90%)">'
files = sorted(glob("fine/*.svg"))

for f in files:
	# o += f'<img width="64" height="64" style="border:1px solid black;" src="{f}">'
	# o += '</img>'
	o += f'<svg width="64" height="64" style="border:1px solid black;">'
	o += f'<text x="1" y="7" fill="gray" font-size="8" font-family="monospace">{hex(int(os.path.basename(f)[0:5]))[2:]}</text>'
	o += open(f,'r').read().replace('width="512.000000pt" height="512.000000pt"','width="64" height="64"')
	o += '</svg>'
o += '</body>/</html>'

print(o)