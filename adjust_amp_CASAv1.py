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
scaler = float(sys.argv[sys.argv.index('adjust_amp_CASAv1.py')+3])

if mode =='scale':
	wscale = scaler
	if(wscale==1.):
		casalog.post('Will leave the amplitudes for this MS unchanged.', 'INFO')
	else:
		casalog.post('Scaling amplitudes for first MS by factor '+str(wscale), 'INFO')
		t.open(theconcatvis, nomodify=False)
		for colname in ['AMPLITUDE']:
			if (colname in t.colnames()) and (t.iscelldefined(colname,0)):
				for j in xrange(0,t.nrows()):
					a = t.getcell(colname, j)
					a *= wscale
					t.putcell(colname, j, a)
		t.close()


elif mode == 'printwt':
	msfile1 = sys.argv[sys.argv.index('wt_mod_CASAv2.py')+2]
	print 'mode = printwt, printing sum of gridded weights in '+msfile1
	tb.open(msfile1)
	print 'wt sum = '+str(np.sum(tb.getcol('WEIGHT')))
	tb.close()

else:
	print 'mode must be printwt or scale'
