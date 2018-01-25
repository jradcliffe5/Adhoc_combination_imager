import os, re
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

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

if ',' in str(inputs['scale']):
    scale = inputs['scale'].split(',')
    scale = [float(i) for i in scale]
else:
    scale = [float(inputs['scale'])]

path_to_ms1 = str(inputs['path_to_ms1'])
path_to_ms2 = str(inputs['path_to_ms2'])
path_to_casa = str(inputs['path_to_casa'])
if ',' in str(inputs['ms2']):
    ms2 = inputs['ms2'].split(',')
    ms2_name = '_'.join([i.split('.ms')[0] for i in ms2])
    ms2_inp = ' '.join(ms2)
    print ms2_inp
else:
    ms2 = str(inputs['ms2'])
    ms2name = ms2.split('.ms')[0]

ms1 = str(inputs['ms1'])

major = []
minor = []
weighting = []
rms = np.array([])
f = open('combination_information_%s_%s.csv' % (ms1.split('.ms')[0],ms2_name),'w')
f.write('weight,rms,bmaj,bmin,bpa\n')
f.close()
f= open('combination_information_%s_%s.csv' % (ms1.split('.ms')[0],ms2_name),'a')
for file in os.listdir('./'):
	if file.endswith('.psf'):
		name = file
		print file
                print ms1
		weight2 = name[name.find("%s_" % ms1.split('.ms')[0])+(len(ms1.split('.ms')[0])+1):name.find("_%s_" % ms2_name)]
		print weight2
		weighting = weighting + [float(name[name.find("%s_" % ms1.split('.ms')[0])+(len(ms1.split('.ms')[0])+1):name.find("_%s_" % ms2_name)])]
		x = imhead(file)
		minor = minor + [x['restoringbeam']['major']['value']]
		major = major + [x['restoringbeam']['minor']['value']]
                rms2 = imstat(imagename=file.split('.psf')[0]+'.image',box='20,20,492,492')['rms']
		rms = np.append(rms,[rms2])
                f.write(','.join([weight2,str(rms2[0]), str(x['restoringbeam']['major']['value']),str(x['restoringbeam']['minor']['value']),str(x['restoringbeam']['positionangle']['value'])])+'\n')

print major, minor, weighting
rms = rms*1E6

plt.figure(1)
plt.scatter(weighting,minor,c='b',label='minor axis')
plt.scatter(weighting,major,c='g',label='major axis')
#plt.scatter(xx,yy)
plt.xlabel('Multiplicative Weighting Factor (weight)')
plt.ylabel('PSF FWHM (arcsec)')
plt.xscale('log')
plt.legend(loc='upper left')
plt.savefig('psf_variation_weight_%s_%s.pdf' % (ms1.split('.ms')[0],ms2_name))
plt.clf()

plt.figure(2)
plt.scatter(weighting,rms,c='b',label='minor axis')
#plt.scatter(xx,yy)
plt.xlabel('Multiplicative Weighting Factor (weight)')
plt.ylabel('rms')
plt.xscale('log')
#plt.legend(loc='upper left')
plt.savefig('rms_variation_weight_%s_%s.pdf' % (ms1.split('.ms')[0],ms2_name))
plt.clf()

plt.figure(3)
plt.scatter(np.sqrt(weighting),minor,c='b',label='minor axis')
plt.scatter(np.sqrt(weighting),major,c='g',label='major axis')
#plt.scatter(xx,yy)
plt.xlabel('Multiplicative Weighting Factor (sigma)')
plt.ylabel('PSF FWHM (arcsec)')
plt.xscale('log')
plt.legend(loc='upper left')
plt.savefig('psf_variation_sigma_%s_%s.pdf' % (ms1.split('.ms')[0],ms2_name))
plt.clf()

plt.figure(4)
plt.scatter(np.sqrt(weighting),rms,c='b',label='minor axis')
#plt.scatter(xx,yy)
plt.xlabel('Multiplicative Weighting Factor (sigma)')
plt.ylabel('rms')
plt.xscale('log')
#plt.legend(loc='upper left')
plt.savefig('rms_variation_sigma_%s_%s.pdf' % (ms1.split('.ms')[0],ms2_name))
plt.clf()
