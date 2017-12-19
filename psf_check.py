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
print log_name
setup_logging_to_file(log_name)
logging.info('Beginning %s' % os.path.basename(__file__))

### Email credentials
email_creds = headless('mail_passwords.txt')
user = email_creds['username']
pwd = email_creds['pwd']

try:
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

    os.system('rsync -ar --progress %s%s ./' % (path_to_ms2,ms2))
    for i in range(len(scale)):
        if os.path.exists('%s_%s_%s_1_psf_CASA.psf' % (ms1.split('.ms')[0],scale[i],ms2.split('.ms')[0])) == False:
            os.system('rsync -ar --progress %s%s ./' % (path_to_ms1,ms1))
            for file in os.listdir('./'):
                if file==ms1:
                    logging.info('Scaling %s by %.2f' % (ms1,scale[i]))
                    os.system('%scasa --nologger --log2term -c wt_mod_CASAv2.py scale %s %s' % (path_to_casa,file, str(scale[i])))

            logging.info('Imaging %s (scale %.2f) and %s' % (ms1,scale[i],ms2))
            os.system('%smpicasa -n 49 %scasa --nologger --log2term -c tclean.py %s %s %s' % (path_to_casa,path_to_casa,str(scale[i]),ms1,ms2))
            os.system('rm *log')
    gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s RUN SUCCESSFULLY - %s' % (os.path.basename(__file__),platform.node()),\
    body='The code %s has run successfully on %s. \n Please see %s:%s  for the results.\n\n The logger output of %s is as follows:\n\n %s' % (os.path.basename(__file__),datetime.now() - startTime, platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))

except exceptions.Exception as e:
    log_exception(e)
    gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s FAILED - %s' % (os.path.basename(__file__),platform.node()),\
    body='The code %s has failed. \n Please see %s:%s  for the details.\n\n The logger and associated error messages of %s is as follows:\n\n %s' % (os.path.basename(__file__), platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))
