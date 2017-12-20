### Defaults
import os, re, sys, exceptions
### Plotter
import matplotlib.pyplot as plt
### Numerics
import numpy as np
from datetime import datetime
startTime = datetime.now()
### For the emailer and logger
#from code_mailer import setup_logging_to_file, log_exception, gmail_emailer, headless
import platform
import logging

### Setup logger
#log_name = "%s.log" % os.path.basename(__file__).split('.py')[0]
#setup_logging_to_file(log_name)
'''
### Email credentials
email_creds = headless('mail_passwords.txt')
user = email_creds['username']
pwd = email_creds['pwd']
'''
msfiles = ['eMER_L_25JUL2015_UVFIX_PEELED.ms','eMER_L_17JUL2015_UVFIX_PEELED.ms','eMER_L_MAR2013_UVFIX_PEELED.ms']
scales = [0.95,1,5]

try:
    concat(vis=msfiles,concatvis='eMER_L_MAR2013_JUL2015_UVFIX_PEELED.ms',visweightscale=scales)
    #gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s RUN SUCCESSFULLY - %s' % (os.path.basename(__file__),platform.node()),\
    #body='The code %s has run successfully on %s. \n Please see %s:%s  for the results.\n\n The logger output of %s is as follows:\n\n %s' % (os.path.basename(__file__),datetime.now() - startTime, platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))

except exceptions.Exception as e:
    log_exception(e)

    #gmail_emailer(user=user,pwd=pwd,recipient='j.f.radcliffe@rug.nl',subject='CODE %s FAILED - %s' % (os.path.basename(__file__),platform.node()),\
    #body='The code %s has failed. \n Please see %s:%s  for the details.\n\n The logger and associated error messages of %s is as follows:\n\n %s' % (os.path.basename(__file__), platform.node(),os.path.dirname(os.path.realpath(__file__)), log_name, open(log_name,'r').read()))
