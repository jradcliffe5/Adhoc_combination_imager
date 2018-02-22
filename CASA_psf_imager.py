import os

tclean(vis=['eMER_L_DR1_PEELED_AMPCOR_LLRR.ms','merge_merlin_FXPOL_reweigh.ms','merge_vla_FXPOL_reweigh.ms','JVLA_all_uvfix.ms'], imsize=[2048,2048], cell=['0.005arcsec','0.005arcsec'], parallel=True, imagename='psf_oversample_large',niter=0)
