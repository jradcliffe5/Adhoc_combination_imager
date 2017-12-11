import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

major = []
minor = []
weighting = []
rms = np.array([])
f = open('combination_information.csv','w')
f.write('weight,rms,bmaj,bmin,bpa\n')
f.close()
f= open('combination_information.csv','a')
for file in os.listdir('./'):
	if file.endswith('.psf'):
		name = file
		print file
		weight2 = name[name.find("ms1_")+4:name.find("_ms2_")]
		print weight2
		weighting = weighting + [float(name[name.find("ms1_")+4:name.find("_ms2_")])]
		x = imhead(file)
		minor = minor + [x['restoringbeam']['major']['value']]
		major = major + [x['restoringbeam']['minor']['value']]
                rms2 = imstat(imagename=file.split('.psf')[0]+'.image',box='20,20,492,492')['rms']
		rms = np.append(rms,[rms2])
                f.write(','.join([weight2,str(rms2[0]), str(x['restoringbeam']['major']['value']),str(x['restoringbeam']['minor']['value']),str(x['restoringbeam']['positionangle']['value'])])+'\n')


print major, minor, weighting
rms = rms*1E6
def func(x,a,c,d):
	return a*np.exp(-c*x)+d

#popt, pcov = curve_fit(func,weighting,minor)
#xx = np.linspace(0,200,1000)
#yy = func(xx,*popt)
plt.figure(1)
plt.scatter(weighting,minor,c='b',label='minor axis')
plt.scatter(weighting,major,c='g',label='major axis')
#plt.scatter(xx,yy)
plt.xlabel('Multiplicative Weighting Factor (weight)')
plt.ylabel('PSF FWHM (arcsec)')
plt.xscale('log')
plt.legend(loc='upper left')
plt.savefig('psf_variation_weight.pdf')
plt.show()

plt.figure(2)
plt.scatter(weighting,rms,c='b',label='minor axis')
#plt.scatter(xx,yy)
plt.xlabel('Multiplicative Weighting Factor (weight)')
plt.ylabel('rms')
plt.xscale('log')
#plt.legend(loc='upper left')
plt.savefig('rms_variation_weight.pdf')
plt.show()

plt.figure(3)
plt.scatter(np.sqrt(weighting),minor,c='b',label='minor axis')
plt.scatter(np.sqrt(weighting),major,c='g',label='major axis')
#plt.scatter(xx,yy)
plt.xlabel('Multiplicative Weighting Factor (sigma)')
plt.ylabel('PSF FWHM (arcsec)')
plt.xscale('log')
plt.legend(loc='upper left')
plt.savefig('psf_variation_sigma.pdf')
plt.show()

plt.figure(4)
plt.scatter(np.sqrt(weighting),rms,c='b',label='minor axis')
#plt.scatter(xx,yy)
plt.xlabel('Multiplicative Weighting Factor (weight)')
plt.ylabel('rms')
plt.xscale('log')
#plt.legend(loc='upper left')
plt.savefig('rms_variation_sigma.pdf')
plt.show()
