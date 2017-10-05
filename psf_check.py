import os, sys

scale = [0.01,0.1,10,100,10000]

for i in range(len(scale)):
	#os.system('rsync -ar --progress UV_data/*ms ./')
	for file in os.listdir('./'):
		print file
		if file.endswith('.ms') and file.startswith('17JUL2015'):
			os.system('casa-release-5.1.0-74.el7/bin/casa --nologger --log2term -c wt_mod_CASAv1.py scale '+file+' '+str(scale[i]))
	os.system('casa-release-5.1.0-74.el7/bin/mpicasa -n 24 casa-release-5.1.0-74.el7/bin/casa --nologger --log2term -c tclean.py '+str(scale[i]))
	os.system('rm *log')
