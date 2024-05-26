# Stefan Nielsen 2020 - various lib import and function definitions:
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from numpy import arange
from IPython import display
from matplotlib.widgets import Button, TextBox
from ipywidgets import Button, HBox, VBox, widgets
import time,pickle,copy
from operator import itemgetter 
import pandas as pd
import obspy 
from obspy.core import read as oread
import sys
import warnings
import subprocess
warnings.filterwarnings("ignore")
###################################
def onclick(event,pos):
    if event.button == 3: 
        pos.append([event.xdata,event.ydata])
        plt.text(event.xdata, event.ydata, 'o', color='r',weight='bold',\
        horizontalalignment='center',verticalalignment='center')
        print([event.xdata,event.ydata])
###################################
def wiggle_plot(dat2, gpos, dx, date, path, infile, pos, shotx, movedgeo, newpos, fig,
               dt=0.004, normalize=False, scale=1., AGC=-1.,redvel=0.0, clip=False):
    # Show seismic traces from all geophones together to allow for picking 
    # The input is 2D numpy array "shotgather" of shape = [NTimes, NTraces]  
    # dt        : time strampling interval (s)
    # gpos      : vector containing the positions of the geophones
    # spacing   : the geophone spacing 'normally' used in this gather, although it may vary in gpos
    # scale     : tramplification factor of each trace in the plot
    # normalize : if True, normalizes each trace in the shotgather using individual trace max/min
    # AGC       : introduces Automatic Gain Control of length AGC. Ignored if AGC = 0
    # redvel    : reduced velocity to try to fit given arrivals. Ignored if redvel = 0
    # clip      : whether to clip higher tramplitudes in plotting the wiggles
    #--------------------------------------------------------------------------------------------
    import numpy as np
    
    def max_rolling1(a, window,axis =1):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        rolling = np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
        return np.max(rolling,axis=axis)
    def rms_rolling(a, window):
        asq=a**2
        rrms=np.zeros(len(a))
        for i in range(window//2,len(a)-(window-1)//2):
            rva=np.sum(asq[i-window//2:i+(window-1)//2])
            rva=np.sqrt(rva/window)
            rrms[i]=rva
        return rrms
        
    NTimes, NTraces = dat2.shape
    if NTraces < 1 or NTimes < 1:
        raise IndexError("Error: trying to process empty array")
    times = np.linspace(0, dt*NTimes, NTimes)
    shift = dx*float((NTraces-0)/NTraces)
    slowness=0.0;tlab='t (s)'
    if redvel != 0.0: slowness = 1./redvel; tlab='t - x/%d (s)'% redvel
    plt.xlim(0, NTraces)
    if AGC > 0:
        nlen=int(AGC/dt)
        if nlen < 1:
            print('ERROR: length of AGC window is too small (<dt)!')
            sys.exit(1)
    tramp = 1.; allmin = 0.; toff = 0.  # initial reference values
    for i, trace in enumerate(dat2.transpose()):
        if AGC > 0:
            trace_sq=trace**2
            trace_rrms=np.convolve(trace_sq, np.ones(nlen), 'same') / float(nlen)
            tr1=np.where(trace_rrms > 0,np.sqrt(trace_rrms), 1.0)
            tr0=trace/tr1
        else:
            tr0=trace
        if normalize:
            allmax = max(tr0.min(), tr0.max(), key=abs)
            allmin = tr0.min()
            tramp=abs(allmax-allmin)
            if (tramp==0): 
                if (allmax == 0): tramp=1
                else: tramp=abs(allmax)
            toff = 0.0
        tr = ((tr0/tramp)-toff)*scale*shift
        if clip:
            for j in range(len(tr)):
                if abs(tr[j]) > shift/2: tr[j]=np.sign(tr[j])*shift/2
        xpos=gpos[i]
        t0=times-xpos*slowness
        plt.plot(xpos+tr*0.0, t0, 'lightgrey')
        plt.plot(xpos+tr, t0, 'k')
        plt.fill_betweenx(t0, xpos, xpos+tr, tr > 0 , color='k')
    plt.xlim(left=-shift,right=xpos+shift)
    plt.ylim(top=-20*dt, bottom = max(times))
    plt.ylabel(tlab)
    plt.xlabel('position (m)')
    tit = date+' ('+infile+')'
    plt.title(tit)
    #button = widgets.Button(description='Update setup', button_style = 'danger')
    #button.on_click(fpath, dat_file, shot_pos, geo_dx, moved_geo, new_pos)
    #VBox([button])
###########################################
def update_shot(fpath, dat_file, shot_pos, geo_dx, moved_geo, new_pos):
    path=fpath.value; infile=dat_file.value;shotx=shot_pos.value; 
    dx=float(geo_dx.value); movedgeo= moved_geo.value; newpos=new_pos.value
    dat1=oread(path+infile)
    dat2=np.transpose(np.array(dat1))
    npts, ntraces = dat2.shape
    dt=1.0/dat1[0].stats.sampling_rate
    date=str(dat1[0].stats.starttime)[0:9];
    flag=True
    try:
        mog = [int(movedgeo),int(newpos)]
    except ValueError:
        mog = [-1,-1]
    gpos=[]
    for i in range(ntraces):
        if i+1 == mog[0]: 
            gpos.append(mog[1])
        else:
            gpos.append(dx*float(i))
    return(dat2, path, infile, gpos, shotx, movedgeo, newpos, dx, dt, date)
##########################################
def box_widget():
    words = ['path to file', 'dat file name', 'shot position', 'geophone spacing', 
         'moved geophone nr.', 'alt geo position (m)']
    #items = [Button(description=w) for w in words]
    items = [widgets.Label(str(i)) for i in words]
    fpath    = widgets.Text('./ExampleData/') # path to folder
    dat_file = widgets.Text('1042.DAT') # name of input data file
    shot_pos = widgets.Text('0.0') # shot position
    geo_dx= widgets.Text('6.0') # geophone spacing
    moved_geo= widgets.Text('None')
    new_pos  = widgets.Text('None')
    dummy = widgets.Text('')
    title2 = '1) Edit name and parameters for shot gather input file:'
    label2 = widgets.Label(value = title2, style=dict(
    	    font_style='bold',font_family = 'Sans',font_size = '32px', #font_variant="small-caps", 
    	    text_color='black'
    	     ))

    lin_0 = HBox([label2])
    col_1 = VBox([items[0], items[1], items[2], items[3], items[4], items[5]])
    col_2 = VBox([fpath,dat_file, shot_pos, geo_dx, moved_geo, new_pos])
    
    return(lin_0, col_1, col_2, fpath, dat_file, shot_pos, geo_dx, moved_geo, new_pos, dummy)
#############################################
def save_pick(pos, gpos, dat_file, fpath, shot_pos, moved_geo, new_pos, fig):
    # quantize position to nearest geophone:
    apos=np.asarray(pos);cpos=[]
    in_file = dat_file.value
    path = fpath.value
    movedgeo= moved_geo.value
    newpos = new_pos.value
    shot_x = shot_pos.value
    for val in apos:
        idx = (np.abs(gpos - val[0])).argmin()
        xx = gpos[idx]
        cpos.append([xx,val[1]])
    cpos=sorted(cpos, key=lambda x: x[0])
    cpos=np.asarray(cpos)
    
    df=pd.DataFrame(cpos);
    # save to file --output name same as input but with "artimes_" in front and ".csv" extension.
    out_file=path+"artimesB_"+in_file[:-4]+".csv"
    f = open(out_file,'w')
    first_line =' '.join([str(shot_x),   ', position of shot. (Note: moved geophone', 
                          str(movedgeo), ' to alternate position:', str(newpos), ')\n'])
    f.write(first_line)
    df.to_csv(f,header=None,index=None)
    f.close()
    # save picking graphic
    fig.savefig(path+"artimes_"+in_file[:-4]+".pdf")
    
