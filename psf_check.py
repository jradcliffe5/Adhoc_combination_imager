import os, sys

scale = [1,10,20,30,40,50,60,70]

for i in range(len(scale)):
	os.system('rsync -ar --progress ../JVLA?_peeled_uvsub_mtmfsub_eMERGE_DR1_averaged_LLRR_uvfix.ms ./')
	for file in os.listdir('./'):
		if file.endswith('.ms') and file.startswith('JVLA'):
			os.system('casa-release-4.7.1-el7/bin/casa --nologger --log2term -c wt_mod_CASAv1.py scale '+file+' '+str(scale[i]))
	os.system('casa-release-4.7.1-el7/bin/mpicasa -n 24 casa-release-4.7.1-el7/bin/casa --nologger --log2term -c tclean.py '+str(scale[i]))
