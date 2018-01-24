### Defaults
import os, re, sys, exceptions
### Plotter
import matplotlib.pyplot as plt
### Numerics
import numpy as np
from datetime import datetime
startTime = datetime.now()
### For the emailer and logger
from code_mailer import setup_logging_to_file, log_exception, gmail_emailer, headless
import platform
import logging

### Setup logger
log_name = "%s.log" % os.path.basename(__file__).split('.py')[0]
setup_logging_to_file(log_name)
logging.info('Beginning %s' % os.path.basename(__file__))
print 'Beginning %s' % os.path.basename(__file__)

### Email credentials
email_creds = headless('mail_passwords.txt')
user = email_creds['username']
pwd = email_creds['pwd']

try:
    #import pandas as pd
    #### Inputs ####
    wsclean_loc = '/scratch/users/radcliff/wsclean-2.5/build/wsclean'
    ncore = 40
    cell = 0.045 ## in arcsec
    imsize = 15 ## in arcmins
    mem = 40 ##percentage memory
    niter = 100000
    gain = 0.1
    mgain = 0.85
    auto_threshold = 1
    channels_out = 8
    deconvolution_channels = 8
    nterms = 2
    bmaj = 0.186069265
    bmin = 0.175903648
    bpa = -81.94953918
    weight = 'natural'
    msfile = './eMER_L_DR1_PEELED_AMPCOR_LLRR.ms'
    ################

    #df = pd.read_csv('combination_information.csv')
    size_scale = int(imsize*60.*(1./cell))
    inputs = headless('inputs.txt')
    logging.info('Input file read successfully')
    scale = inputs['scale'].split('[')[1].split(']')[0].split(',')
    scale = [float(i) for i in scale]
    print scale
    path_to_ms1 = str(inputs['path_to_ms1'])
    path_to_ms2 = str(inputs['path_to_ms2'])
    path_to_casa = str(inputs['path_to_casa'])
    ms1 = str(inputs['ms1'])
    ms2 = str(inputs['ms2'])
    logging.info('Will scale %s by the following scales: %s' % (ms1, scale))
    '''
    os.system('rsync -ar --progress %s%s ./' % (path_to_ms2,ms2))
    for i in range(len(scale)):
        if os.path.exists('%s_%s_%s_1_psf_CASA.psf' % (ms1.split('.ms')[0],scale[i],ms2.split('.ms')[0])) == False:
            os.system('rsync -ar --progress %s%s ./' % (path_to_ms1,ms1))
            for file in os.listdir('./'):
                if file==ms1:
                    logging.info('Scaling %s by %.2f' % (ms1,scale[i]))
                    os.system('%scasa --nologger --log2term -c wt_mod_CASAv2.py scale %s %s' % (path_to_casa,file, str(scale[i])))
    '''
    logging.info('Running wsclean')
    if bpa < 0:
        bpa = 360+bpa ## command line entry does not accept negatives
    logging.info('wsclean inputs = %s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg -join-channels -channels-out %s -deconvolution-channels %s -fit-spectral-pol %s %s %s' % (wsclean_loc, mem, ncore, msfile.split('.ms')[0]+'.wsclean', size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa, channels_out, deconvolution_channels, nterms, ms1, ms2))
    os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg -join-channels -channels-out %s -deconvolution-channels %s -fit-spectral-pol %s %s %s' % (wsclean_loc,mem, ncore, msfile.split('.ms')[0]+'.wsclean', size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa, channels_out, deconvolution_channels, nterms, ms1, ms2))
    logging.info('COMPLETE... a shiny image is made')

    gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s RUN SUCCESSFULLY - %s' % (os.path.basename(__file__),platform.node()),\
    body='The code %s has run successfully on %s. \n Please see %s:%s  for the results.\n\n The logger output of %s is as follows:\n\n %s' % (os.path.basename(__file__),datetime.now() - startTime, platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))

except exceptions.Exception as e:
    log_exception(e)
    gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s FAILED - %s' % (os.path.basename(__file__),platform.node()),\
    body='The code %s has failed. \n Please see %s:%s  for the details.\n\n The logger and associated error messages of %s is as follows:\n\n %s' % (os.path.basename(__file__), platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))
