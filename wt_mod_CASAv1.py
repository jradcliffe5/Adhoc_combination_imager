#weight scaler for CASA and wsclean usage
#n.b. weight column changes as n, sigma as 1/sqrt(n), wt_sp as n and no change to sig_sp
import numpy as np
import sys
## Inputs ############################################################
'''
tb.open(msfile1,nomodify=False)
msfile1_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
tb.close()
tb.open(msfile2,nomodify=False)
msfile2_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
'''
print sys.argv
mode = sys.argv[sys.argv.index('wt_mod_CASAv1.py')+1]
if mode =='scale':
	msfile1 = sys.argv[sys.argv.index('wt_mod_CASAv1.py')+2]
	scaler = float(sys.argv[sys.argv.index('wt_mod_CASAv1.py')+3])
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

elif mode == 'printwt':
	msfile1 = sys.argv[sys.argv.index('wt_mod_CASAv1.py')+2]
	print 'mode = printwt, printing sum of gridded weights in '+msfile1
	tb.open(msfile1)
	print 'wt sum = '+str(np.sum(tb.getcol('WEIGHT')))
	tb.close()

else:
	print 'mode must be printwt or scale'


