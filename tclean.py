import os
name = sys.argv[sys.argv.index('tclean.py')+4]
cellsize = sys.argv[sys.argv.index('tclean.py')+1]
imsize = sys.argv[sys.argv.index('tclean.py')+2]
phase_center = str(sys.argv[sys.argv.index('tclean.py')+3])
ms1 = sys.argv[sys.argv.index('tclean.py')+5]
ms2 = sys.argv[sys.argv.index('tclean.py')+6:]

vis = [ms1] + ms2
print sys.argv, imsize
ms2_name = '_'.join([i.split('.ms')[0] for i in ms2])

print phase_center

tclean(vis=vis,selectdata=True,field="",spw="",timerange="",uvrange="",\
antenna="",scan="",observation="",intent="",datacolumn="data",imagename='%s_%s_%s_1_psf_CASA' % (ms1.split('.ms')[0],name,ms2_name),\
imsize=[int(imsize),int(imsize)],\
       cell=[cellsize],phasecenter=phase_center,stokes="I",projection="SIN",\
startmodel="",specmode="mfs",reffreq="",\
nchan=-1,start="",width="",outframe="LSRK",veltype="radio",restfreq=[],interpolation="linear" \
,gridder="standard",facets=1,chanchunks=1,\
wprojplanes=1,vptable="",aterm=True,psterm=False,wbawp=True,\
conjbeams=False,cfcache="",computepastep=360.0,\
rotatepastep=360.0,pblimit=0.2,normtype="flatnoise",\
deconvolver="hogbom",scales=[],nterms=2,smallscalebias=0.6,restoration=True,restoringbeam=[],\
pbcor=False,outlierfile="",weighting="natural",\
robust=0.5,npixels=0,uvtaper=[],niter=0,gain=0.1\
,threshold=0.0,cycleniter=-1,cyclefactor=1.0,minpsffraction=0.05,maxpsffraction=0.8,interactive=False\
,usemask="user",mask="",pbmask=0.0,maskthreshold="",maskresolution="",nmask=0,sidelobethreshold=3.0\
,noisethreshold=5.0,lownoisethreshold=1.5,negativethreshold=0.0,smoothfactor=1.0,minbeamfrac=0.3\
,cutthreshold=0.01,growiterations=75,restart=True,savemodel="none",calcres=True,calcpsf=True,parallel=True)
