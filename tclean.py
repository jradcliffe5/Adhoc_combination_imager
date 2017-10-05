name = sys.argv[sys.argv.index('tclean.py')+1]

tclean(vis=['17JUL2015_reway_sc.ms','merge_merlin_FXPOL.ms'],selectdata=True, field="",spw="",timerange="",uvrange="",antenna="",scan="", observation="", intent="",datacolumn="data", imagename='eM'+name+"M1_psf_CASA", imsize=[512, 512], cell="0.05arcsec", phasecenter="",stokes="I",projection="SIN",startmodel="",specmode="mfs",reffreq="",nchan=-1,start="",width="",outframe="LSRK",veltype="radio",restfreq=[],interpolation="linear",gridder="standard",facets=1,chanchunks=1,wprojplanes=1,vptable="", aterm=True,psterm=False,wbawp=True,conjbeams=True,cfcache="",computepastep=360.0, rotatepastep=360.0,pblimit=0.2,normtype="flatnoise",deconvolver="hogbom",scales=[],nterms=2,smallscalebias=0.6,restoration=True,restoringbeam=[],pbcor=False,outlierfile="",weighting="natural",robust=0.5,npixels=0,uvtaper=[],niter=0,gain=0.1,threshold=0.0,cycleniter=-1,cyclefactor=1.0,minpsffraction=0.05,maxpsffraction=0.8,interactive=False,usemask="user",mask="",pbmask=0.0,maskthreshold="",maskresolution="",nmask=0,autoadjust=False,sidelobethreshold=3.0,noisethreshold=3.0,lownoisethreshold=3.0,smoothfactor=1.0,minbeamfrac=-1.0,cutthreshold=0.01,restart=True,savemodel="none",calcres=False,calcpsf=True,parallel=True)
