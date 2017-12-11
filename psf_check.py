import os, sys

### Inputs
scale = [1]
path_to_ms = '../'
path_to_casa = '../casa-release-5.1.1-5.el7/bin/'
ms1 = 'eMER_L_25JUL2015_UVFIX_PEELED.ms'
ms2 = 'eMER_L_17JUL2015_UVFIX_PEELED.ms'

os.system('rsync -ar --progress %s%s ./' % (path_to_ms,ms2))
for i in range(len(scale)):
	os.system('rsync -ar --progress %s%s ./' % (path_to_ms,ms1))
	for file in os.listdir('./'):
		if file==ms1:
			print 'scaling %s by %.2f' % (ms1,scale[i])
			os.system('%scasa --nologger --log2term -c wt_mod_CASAv2.py scale %s %s' % (path_to_casa,file, str(scale[i])))

	os.system('%smpicasa -n 24 %scasa --nologger --log2term -c tclean.py %s %s %s' % (path_to_casa,path_to_casa,str(scale[i]),ms1,ms2))
	os.system('rm *log')
