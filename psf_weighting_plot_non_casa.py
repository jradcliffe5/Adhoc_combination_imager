### Defaults
import os, re, sys, exceptions
### Plotter
import matplotlib.pyplot as plt
### Numerics
import numpy as np
import pandas as pd
from datetime import datetime
startTime = datetime.now()
### For the emailer and logger
from code_mailer import setup_logging_to_file, log_exception, gmail_emailer, headless
import platform
import logging

### Setup logger
log_name = "%s.log" % os.path.basename(__file__).split('.py')[0]
setup_logging_to_file(log_name)

### Email credentials
email_creds = headless('mail_passwords.txt')
user = email_creds['username']
pwd = email_creds['pwd']

try:
    inputs = headless('inputs.txt')
    scale = inputs['scale'].split('[')[1].split(']')[0].split(',')
    scale = [float(i) for i in scale]
    print scale
    path_to_ms1 = str(inputs['path_to_ms1'])
    path_to_ms2 = str(inputs['path_to_ms2'])
    path_to_casa = str(inputs['path_to_casa'])
    ms1 = str(inputs['ms1'])
    ms2 = str(inputs['ms2'])

    df = pd.read_csv('combination_information_%s_%s.csv' % (ms1.split('.ms')[0],ms2.split('.ms')[0]),delimiter=',')

    major = df['bmaj']
    minor = df['bmin']
    weighting = df['weight']
    rms = df['rms']

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
    plt.savefig('psf_variation_weight_%s_%s.pdf' % (ms1.split('.ms')[0],ms2.split('.ms')[0]))
    plt.show()

    plt.figure(2)
    plt.scatter(weighting,rms,c='b',label='minor axis')
    #plt.scatter(xx,yy)
    plt.xlabel('Multiplicative Weighting Factor (weight)')
    plt.ylabel('rms')
    plt.xscale('log')
    #plt.legend(loc='upper left')
    plt.savefig('rms_variation_weight_%s_%s.pdf' % (ms1.split('.ms')[0],ms2.split('.ms')[0]))
    plt.show()

    plt.figure(3)
    plt.scatter(np.sqrt(weighting),minor,c='b',label='minor axis')
    plt.scatter(np.sqrt(weighting),major,c='g',label='major axis')
    #plt.scatter(xx,yy)
    plt.xlabel('Multiplicative Weighting Factor (sigma)')
    plt.ylabel('PSF FWHM (arcsec)')
    plt.xscale('log')
    plt.legend(loc='upper left')
    plt.savefig('psf_variation_sigma_%s_%s.pdf' % (ms1.split('.ms')[0],ms2.split('.ms')[0]))
    plt.show()

    plt.figure(4)
    plt.scatter(np.sqrt(weighting),rms,c='b',label='minor axis')
    #plt.scatter(xx,yy)
    plt.xlabel('Multiplicative Weighting Factor (sigma)')
    plt.ylabel('rms')
    plt.xscale('log')
    #plt.legend(loc='upper left')
    plt.savefig('rms_variation_sigma_%s_%s.pdf' % (ms1.split('.ms')[0],ms2.split('.ms')[0]))
    plt.show()

    gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s RUN SUCCESSFULLY - %s' % (os.path.basename(__file__),platform.node()),\
    body='The code %s has run successfully on %s. \n Please see %s:%s  for the results.\n\n The logger output of %s is as follows:\n\n %s' % (os.path.basename(__file__),datetime.now() - startTime, platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))

except exceptions.Exception as e:
    log_exception(e)
    gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s FAILED - %s' % (os.path.basename(__file__),platform.node()),\
    body='The code %s has failed. \n Please see %s:%s  for the details.\n\n The logger and associated error messages of %s is as follows:\n\n %s' % (os.path.basename(__file__), platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))
