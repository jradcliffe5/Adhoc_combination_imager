#weight scaler for CASA and wsclean usage
#n.b. weight column changes as n, sigma as 1/sqrt(n), wt_sp as n and no change to sig_sp
import numpy as np
## Inputs ############################################################
msfile1 = 'JVLA1_peeled_uvsub_mtmfsub_eMERGE_DR1_averaged_LLRR_uvfix.ms'
msfile2 = '17JUL2015_reway_sc_uvfix_LLRR.ms'
'''
tb.open(msfile1,nomodify=False)
msfile1_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
tb.close()
tb.open(msfile2,nomodify=False)
msfile2_wt_sum = np.sum(tb.getcol('WEIGHT_SPECTRUM'))
'''
scaler = 70
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


