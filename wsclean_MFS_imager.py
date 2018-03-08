## Defaults
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
    inputs = headless('inputs.txt')
    wsclean_loc = str(inputs['wsclean_loc'])
    ncore = int(inputs['ncore'])
    cell = float(inputs['cell']) ## in arcsec
    imsize = float(inputs['imsize']) ## in arcmins
    mem = float(inputs['mem']) ##percentage memory
    niter = int(inputs['niter'])
    gain = float(inputs['gain'])
    mgain = float(inputs['mgain'])
    auto_threshold = float(inputs['auto_threshold'])
    do_MFS = str(inputs['do_MFS'])
    channels_out = int(inputs['channels_out'])
    deconvolution_channels = int(inputs['deconvolution_channels'])
    nterms = int(inputs['nterms'])
    bmaj = float(inputs['bmaj'])
    bmin = float(inputs['bmin'])
    bpa = float(inputs['bpa'])
    weight = str(inputs['weight'])
    do_scale = str(inputs['do_scale'])
    do_multiscale = str(inputs['do_multiscale'])
    multi_scale_scales = str(inputs['multi_scale_scales'])
    ################

    if len(multi_scale_scales) == 0:
        multi_scale_scales = ''
    else:
        multi_scale_scales = '-multiscale-scales %s' % multi_scale_scales

    #df = pd.read_csv('combination_information.csv')
    size_scale = int(imsize*60.*(1./cell))

    logging.info('Input file read successfully')

    scale = [float(inputs['wsclean_scale'])]
    path_to_ms1 = str(inputs['path_to_ms1'])
    path_to_ms2 = str(inputs['path_to_ms2'])
    path_to_casa = str(inputs['path_to_casa'])
    if ',' in str(inputs['ms2']):
        ms2 = inputs['ms2'].split(',')
        ms2_name = '_'.join([i.split('.ms')[0] for i in ms2])
        ms2_inp = ' '.join(ms2)
    else:
        ms2 = str(inputs['ms2'])
        ms2_name = ms2.split('.ms')[0]

    ms1 = str(inputs['ms1'])
    logging.info('Will scale %s by the following scales: %s' % (ms1, scale))

    if len(list(ms2)) > 1:
        for i in ms2:
            os.system('rsync -ar --progress %s%s ./' % (path_to_ms2,i))
    else:
        os.system('rsync -ar --progress %s%s ./' % (path_to_ms2,ms2))
    for i in range(len(scale)):
        if do_scale == 'True':
            os.system('rsync -ar --progress %s%s ./' % (path_to_ms1,ms1))
            for file in os.listdir('./'):
                if file==ms1:
                    logging.info('Scaling %s by %.2f' % (ms1,scale[i]))
                    os.system('%scasa --nologger --log2term -c wt_mod_CASAv2.py scale %s %s' % (path_to_casa,file, str(scale[i])))

    logging.info('Running wsclean')
    if bpa < 0:
        bpa = 360+bpa ## command line entry does not accept negatives

    if do_MFS == 'True':
        if do_multiscale == 'True':
            logging.info('wsclean inputs = %s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg -join-channels -channels-out %s -deconvolution-channels %s -fit-spectral-pol %s -multiscale %s %s %s' % (wsclean_loc, mem, ncore,'%s_%s_%s_1.wsclean' % (ms1.split('.ms')[0],scale[i],ms2_name), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa, channels_out, deconvolution_channels, nterms, multi_scale_scales, ms1, ms2_inp))
            os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg -join-channels -channels-out %s -deconvolution-channels %s -fit-spectral-pol %s -multiscale %s %s %s' % (wsclean_loc,mem, ncore, '%s_%s_%s_1.wsclean' % (ms1.split('.ms')[0],scale[i],ms2_name), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa, channels_out, deconvolution_channels, nterms, multi_scale_scales, ms1, ms2_inp))
        else:
            logging.info('wsclean inputs = %s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg -join-channels -channels-out %s -deconvolution-channels %s -fit-spectral-pol %s %s %s' % (wsclean_loc, mem, ncore,'%s_%s_%s_1.wsclean' % (ms1.split('.ms')[0],scale[i],ms2_name), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa, channels_out, deconvolution_channels, nterms, ms1, ms2_inp))
            os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg -join-channels -channels-out %s -deconvolution-channels %s -fit-spectral-pol %s %s %s' % (wsclean_loc,mem, ncore, '%s_%s_%s_1.wsclean' % (ms1.split('.ms')[0],scale[i],ms2_name), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa, channels_out, deconvolution_channels, nterms, ms1, ms2_inp))
        logging.info('COMPLETE... a shiny image is made')
    else:
        if do_multiscale == 'True':
            logging.info('wsclean inputs = %s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg -multiscale %s %s %s' % (wsclean_loc, mem, ncore,'%s_%s_%s_1.wsclean' % (ms1.split('.ms')[0],scale[i],ms2_name), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa,multi_scale_scales, ms1, ms2_inp))
            os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg -multiscale %s %s %s' % (wsclean_loc,mem, ncore, '%s_%s_%s_1.wsclean' % (ms1.split('.ms')[0],scale[i],ms2_name), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa,multi_scale_scales, ms1, ms2_inp))
            logging.info('COMPLETE... a shiny image is made')
        else:
            logging.info('wsclean inputs = %s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg %s %s' % (wsclean_loc, mem, ncore,'%s_%s_%s_1.wsclean' % (ms1.split('.ms')[0],scale[i],ms2_name), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa, ms1, ms2_inp))
            os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -beam-shape %sasec %sasec %sdeg %s %s' % (wsclean_loc,mem, ncore, '%s_%s_%s_1.wsclean' % (ms1.split('.ms')[0],scale[i],ms2_name), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, bmaj, bmin, bpa, ms1, ms2_inp))
            logging.info('COMPLETE... a shiny image is made')

    gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s RUN SUCCESSFULLY - %s' % (os.path.basename(__file__),platform.node()),\
    body='The code %s has run successfully on %s. \n Please see %s:%s  for the results.\n\n The logger output of %s is as follows:\n\n %s' % (os.path.basename(__file__),datetime.now() - startTime, platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))

except exceptions.Exception as e:
    log_exception(e)
    gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s FAILED - %s' % (os.path.basename(__file__),platform.node()),\
    body='The code %s has failed. \n Please see %s:%s  for the details.\n\n The logger and associated error messages of %s is as follows:\n\n %s' % (os.path.basename(__file__), platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))
