#weight scaler for CASA and wsclean usage
#n.b. weight column changes as n, sigma as 1/sqrt(n), wt_sp as n and no change to sig_sp
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
mode = sys.argv[sys.argv.index(sys.argv[2])+1]
theconcatvis = sys.argv[sys.argv.index(sys.argv[2])+2]
scaler = float(sys.argv[sys.argv.index(sys.argv[2])+3])

if mode =='scale':
	wscale = scaler
	if(wscale==1.):
		casalog.post('Will leave the weights for this MS unchanged.', 'INFO')
	else:
		casalog.post('Scaling weights for first MS by factor '+str(wscale), 'INFO')
		t.open(theconcatvis, nomodify=False)
		for colname in [ 'WEIGHT', 'WEIGHT_SPECTRUM']:
			if (colname in t.colnames()) and (t.iscelldefined(colname,0)):
				for j in xrange(0,t.nrows()):
					a = t.getcell(colname, j)
					a *= wscale
					t.putcell(colname, j, a)
		for colname in ['SIGMA']:
			if (wscale > 0. and colname in t.colnames()) and (t.iscelldefined(colname,0)):
				sscale = 1./sqrt(wscale)
				for j in xrange(0,t.nrows()):
					a = t.getcell(colname, j)
					a *= sscale
					t.putcell(colname, j, a)
		t.close()

elif mode =='scaleconcat':
	wscale = scaler
	ms2 = str(sys.argv[sys.argv.index('wt_mod_CASAv2.py')+4])
	output_ms = str(sys.argv[sys.argv.index('wt_mod_CASAv2.py')+5])
	if(wscale==1.):
		casalog.post('Will leave the weights for this MS unchanged.', 'INFO')
	else:
		casalog.post('Scaling weights for first MS by factor '+str(wscale), 'INFO')
		t.open(theconcatvis, nomodify=False)
		for colname in [ 'WEIGHT', 'WEIGHT_SPECTRUM']:
			if (colname in t.colnames()) and (t.iscelldefined(colname,0)):
				for j in xrange(0,t.nrows()):
					a = t.getcell(colname, j)
					a *= wscale
					t.putcell(colname, j, a)
		for colname in ['SIGMA']:
			if (wscale > 0. and colname in t.colnames()) and (t.iscelldefined(colname,0)):
				sscale = 1./sqrt(wscale)
				for j in xrange(0,t.nrows()):
					a = t.getcell(colname, j)
					a *= sscale
					t.putcell(colname, j, a)
		t.close()
	concat(vis=[theconcatvis,ms2],concatvis=output_ms)


	'''
	msfile1 = sys.argv[sys.argv.index('wt_mod_CASAv1.py')+2]
	scaler = float(sys.argv[sys.argv.index('wt_mod_CASAv1.py')+3])**2
	print scaler
	 #this is the square of the rms sensitivities
	######################################################################
	tb.open(msfile1,nomodify=False)
	weight = (tb.getcol('WEIGHT'))*scaler
	sigma = (tb.getcol('SIGMA'))*(1/(np.sqrt(scaler)))
	wt_spectrum = (tb.getcol('WEIGHT_SPECTRUM'))*scaler

	tb.putcol('WEIGHT',weight)
	tb.putcol('SIGMA',sigma)
	tb.putcol('WEIGHT_SPECTRUM',wt_spectrum)
	tb.close()
	'''
elif mode == 'printwt':
	msfile1 = sys.argv[sys.argv.index('wt_mod_CASAv2.py')+2]
	print 'mode = printwt, printing sum of gridded weights in '+msfile1
	tb.open(msfile1)
	print 'wt sum = '+str(np.sum(tb.getcol('WEIGHT')))
	tb.close()

else:
	print 'mode must be printwt or scale'
