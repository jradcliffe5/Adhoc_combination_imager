#weight scaler for CASA and wsclean usage
#n.b. weight column changes as n, sigma as 1/sqrt(n), wt_sp as n and no change to sig_sp
import numpy as np
import sys
## Inputs ############################################################
msfile = sys.argv[5:]
print msfile
######################################################################
msfiles_wt_sum = []
for i in range(len(msfile)):
	tb.open(msfile[i],nomodify=False)
	msfiles_wt_sum = msfiles_wt_sum + [np.sum(tb.getcol('WEIGHT'))]
	tb.close()
	print 'Gridded weights of '+msfile[i]+':'+str(msfiles_wt_sum[i])

max_wt_sum = np.max(msfiles_wt_sum)
max_wt_sum_index = np.argwhere(msfiles_wt_sum==max_wt_sum)

print 'Maximum sum of weights = '+str(max_wt_sum)+' in measurement set: '+msfile[i]
scaler = max_wt_sum/msfiles_wt_sum
for i in range(len(msfile)):
	print 'MS: '+msfile[i]+' Scaling factor: '+str(scaler[i])

 #this is the square of the rms sensitivities
######################################################################
for i in range(len(msfile)):
	tb.open(msfile[i],nomodify=False)
	weight = (tb.getcol('WEIGHT'))*scaler[i]
	sigma = (tb.getcol('SIGMA'))*(1/np.sqrt(scaler[i]))
	try:
		wt_spectrum = (tb.getcol('WEIGHT_SPECTRUM'))*scaler[i]
	except RuntimeError:
		pass
	try:
		si_spectrum = (tb.getcol('SIGMA_SPECTRUM'))*(1/np.sqrt(scaler[i]))
	except RuntimeError:
		pass
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

