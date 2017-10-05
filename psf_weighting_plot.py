import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

major = []
minor = []
weighting = []
for file in os.listdir('./'):
	if file.endswith('.psf'):
		name = file
		weighting = weighting + [int(name[name.find("J")+1:name.find("e")])]
		x = imhead(file)
		minor = minor + [x['restoringbeam']['major']['value']]
		major = major + [x['restoringbeam']['minor']['value']]

print major, minor, weighting

def func(x,a,c,d):
	return a*np.exp(-c*x)+d

#popt, pcov = curve_fit(func,weighting,minor)
#xx = np.linspace(0,200,1000)
#yy = func(xx,*popt)
plt.figure(1)
plt.scatter(weighting,minor,c='b',label='minor axis')
plt.scatter(weighting,major,c='g',label='major axis')
#plt.scatter(xx,yy)
plt.xlabel('JVLA Multiplicative Weighting Factor (weight)')
plt.ylabel('PSF FWHM (arcsec)')
#plt.xscale('log')
plt.legend(loc='upper left')
plt.savefig('psf_variation_weight_JVLA_eMERLIN.pdf')
plt.show()

plt.figure(2)
plt.scatter(np.sqrt(weighting),minor,c='b',label='minor axis')
plt.scatter(np.sqrt(weighting),major,c='g',label='major axis')
#plt.scatter(xx,yy)
plt.xlabel('JVLA Multiplicative Weighting Factor (sigma)')
plt.ylabel('PSF FWHM (arcsec)')
#plt.xscale('log')
plt.legend(loc='upper left')
plt.savefig('psf_variation_sigma_JVLA_eMERLIN.pdf')
plt.show()
