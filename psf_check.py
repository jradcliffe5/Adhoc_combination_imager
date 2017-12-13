import os, sys
import re

### Inputs
def headless(inputfile):
    ''' Parse the list of inputs given in the specified file. (Modified from evn_funcs.py)'''
    INPUTFILE = open(inputfile, "r")
    control = {}
    # a few useful regular expressions
    newline = re.compile(r'\n')
    space = re.compile(r'\s')
    char = re.compile(r'\w')
    comment = re.compile(r'#.*')
    # parse the input file assuming '=' is used to separate names from values
    for line in INPUTFILE:
        if char.match(line):
            line = comment.sub(r'', line)
            line = line.replace("'", '')
            (param, value) = line.split('=')
            param = newline.sub(r'', param)
            param = param.strip()
            param = space.sub(r'', param)
            value = newline.sub(r'', value)
            value = value.replace(' ','').strip()
            valuelist = value.split(',')
            if len(valuelist) == 1:
                if valuelist[0] == '0' or valuelist[0]=='1' or valuelist[0]=='2':
                    control[param] = int(valuelist[0])
                else:
                    control[param] = str(valuelist[0])
            else:
                control[param] = ','.join(valuelist)
    return control

inputs = headless('inputs.txt')
scale = inputs['scale'].split('[')[1].split(']')[0].split(',')
scale = [float(i) for i in scale]
print scale
path_to_ms = str(inputs['path_to_ms'])
path_to_casa = str(inputs['path_to_casa'])
ms1 = str(inputs['ms1'])
ms2 = str(inputs['ms2'])

os.system('rsync -ar --progress %s%s ./' % (path_to_ms,ms2))
for i in range(len(scale)):
    if os.path.exists('%s_%s_%s_1_psf_CASA.psf' % (ms1.split('.ms')[0],scale[i],ms2.split('.ms')[0])) == False:
        print '%s_%s_%s_1_psf_CASA.psf' % (ms1.split('.ms')[0],scale[i],ms2.split('.ms')[0])
        
    	os.system('rsync -ar --progress %s%s ./' % (path_to_ms,ms1))
    	for file in os.listdir('./'):
    		if file==ms1:
    			print 'scaling %s by %.2f' % (ms1,scale[i])
    			os.system('%scasa --nologger --log2term -c wt_mod_CASAv2.py scale %s %s' % (path_to_casa,file, str(scale[i])))

    	os.system('%smpicasa -n 24 %scasa --nologger --log2term -c tclean.py %s %s %s' % (path_to_casa,path_to_casa,str(scale[i]),ms1,ms2))
    	os.system('rm *log')
        
