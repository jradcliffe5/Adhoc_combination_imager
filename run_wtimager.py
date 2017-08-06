import os, sys

scale = 5
for file in os.listdir('./'):
	if file.endswith('.ms') and file.startswith('JVLA'):
		os.system('casa --nologger --log2term -c wt_mod_CASAv1.py scale '+file+' '+str(scale))

os.system('wsclean-2.2 -j 12 -name J'+str(scale)+'eM1 -size 512 512 -niter 100 -scale 0.05asec -weight natural *LLRR_uvfix.ms eMERLIN_DR1_all.ms' )
