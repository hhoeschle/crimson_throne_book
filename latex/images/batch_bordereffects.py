import glob
import os

for jpg in glob.glob('*.jpg'):
	if '_mod.jpg' not in jpg:
		print jpg 
		jpg_mod = jpg[:-4] +'_mod.jpg'
		print jpg_mod
		cmd = './bordereffects -s 2 -d 1 -c 5 -g 1 -p 2 -b white ' + jpg + ' ' + jpg_mod
		print cmd
		os.system(cmd)