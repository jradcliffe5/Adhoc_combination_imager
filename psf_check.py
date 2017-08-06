import os, sys

scale = [13]

for i in range(len(scale)):
	os.system('rsync -ar --progress UV_data/*ms ./')
	for file in os.listdir('./'):
		if file.endswith('.ms') and file.startswith('J123642_621331_uvfix'):
			os.system('casa-release-4.7.1-el7/bin/casa --nologger --log2term -c wt_mod_CASAv1.py scale '+file+' '+str(scale[i]))
	os.system('casa-release-4.7.1-el7/bin/mpicasa -n 24 casa-release-4.7.1-el7/bin/casa --nologger --log2term -c tclean.py '+str(scale[i]))
	os.system('rm *log')
