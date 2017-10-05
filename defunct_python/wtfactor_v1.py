#weight scaler for CASA and wsclean usage
#n.b. weight column changes as n, sigma as 1/sqrt(n), wt_sp as n and no change to sig_sp
import numpy as np
## Inputs ############################################################
msfile1 = 'merge_vla_FXPOL.ms'
msfile2 = 'merge_merlin_FXPOL.ms'

tb.open(msfile1,nomodify=False)
msfile1_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
tb.close()
print 'Gridded weights of '+msfile1+':'+str(msfile1_wt_sum)
tb.open(msfile2,nomodify=False)
msfile2_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
tb.close()
print 'Gridded weights of '+msfile2+':'+str(msfile2_wt_sum)
scaler = msfile2_wt_sum/msfile1_wt_sum
print 'Ratio of '+msfile2+'/'+msfile1+' = '+str(scaler)
 #this is the square of the rms sensitivities
######################################################################
tb.open(msfile1,nomodify=False)
weight = (tb.getcol('WEIGHT'))*scaler
sigma = (tb.getcol('SIGMA'))*(1/np.sqrt(scaler))
try:
	wt_spectrum = (tb.getcol('WEIGHT_SPECTRUM'))*scaler
except RuntimeError:
	pass
try:
	si_spectrum = (tb.getcol('SIGMA_SPECTRUM'))*(1/np.sqrt(scaler))
except RuntimeError

tb.putcol('WEIGHT',weight)
tb.putcol('SIGMA',sigma)
try:
	tb.putcol('WEIGHT_SPECTRUM',wt_spectrum)
except RuntimeError,NameError:
	pass
try:
	tb.putcol('SIGMA_SPECTRUM',si_spectrum)
except RuntimeError,NameError:
	pass
tb.close()


