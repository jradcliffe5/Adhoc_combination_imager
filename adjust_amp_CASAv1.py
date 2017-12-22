#amplitude scaler for CASA and wsclean usage
import numpy as np
import sys
import os
import shutil
import stat
import time
from math import sqrt
from taskinit import *

t = tbtool()
## Inputs ############################################################
'''
tb.open(msfile1,nomodify=False)
msfile1_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
tb.close()
tb.open(msfile2,nomodify=False)
msfile2_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
'''
print sys.argv
mode = sys.argv[sys.argv.index('adjust_amp_CASAv1.py')+1]
theconcatvis = sys.argv[sys.argv.index('adjust_amp_CASAv1.py')+2]
delete = sys.argv[sys.argv.index('adjust_amp_CASAv1.py')+3]
scaler = float(sys.argv[sys.argv.index('adjust_amp_CASAv1.py')+4])


if mode =='scale':
	wscale = scaler
	if(wscale==1.):
		casalog.post('Will leave the amplitudes for this MS unchanged.', 'INFO')
	else:
		casalog.post('Using gencal to scale amplitudes for first MS by factor '+str(wscale), 'INFO')
		os.system('rm -r %s.amp%s_adj' % (theconcatvis,wscale))
		gencal(vis=theconcatvis,caltable='%s.amp%s_adj' % (theconcatvis,wscale),caltype='amp',parameter=[wscale])
		applycal(vis=theconcatvis,gaintable='%s.amp%s_adj' % (theconcatvis,wscale), applymode='calonly')
		splitname=theconcatvis.split('.ms')[0]+'_split.ms'
		split(vis=theconcatvis, outputvis=splitname)
		if delete == 'T':
			os.system('rm -r %s' % theconcatvis)
			os.system('mv %s %s' % (splitname,theconcatvis))
		else:
			clearcal(theconcatvis)
			os.system('mv %s %s' % (splitname,splitname.split('.ms')[0]+'a%s.ms' % wscale))
