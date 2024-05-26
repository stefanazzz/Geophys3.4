import matplotlib.pyplot as plt
import pygimli as pg
from pygimli.physics import Refraction, TravelTimeManager
from ipywidgets import Button, HBox, VBox, widgets, Output
import numpy as np
import pandas as pd
import ast
#from IPython.display import display,clear_output

#

def update_dict(): # Store the refreshed input values for filenames, path, error to use next runtime
    details={'path': fpath.value,
             'project_name': uni2file.value,
             'error': aerr.value,
             'files': [fna.value for fna in fnames]}
    f = open("dict.yml", 'w')
    f.write(str(details))
    f.close()
#

def sort_list(): # sort all positions of geos and sources found in artime files
    err = float(aerr.value); path = fpath.value;
    file_names=[];allpos=[];file_shotpos=[];
    for fi in fnames:
        if fi.value != '':
            file_names.append(fi.value)
    for i in file_names:
        fil=path+i
        fn=open(fil,'r')
        shot_pos=float(fn.readline().split(',')[0])
        allpos.append(shot_pos)
        file_shotpos.append([shot_pos, i])
        #print(fil,shot_pos)
        pps=fn.readlines()
        for pp in pps:
            gpos=float(pp.split(',')[0])
            allpos.append(gpos)
        fn.close()
    allpos=sorted(set(allpos))
    npos=len(allpos)
    allpos=np.array([allpos, np.zeros(npos)]).T
    df=pd.DataFrame(allpos)
    with open('allpos.csv', 'w') as file:
        he = str(npos)+'\n'
        file.write(he)
        df.to_csv(file, header=None, index=False)
    df=pd.DataFrame(file_shotpos)
    df.to_csv('file_shotpos.csv', header=None, index=False)
    print('... updated')
    print('if needed modify topography in second column of file \'allpos.csv\'')
    sort_list.data=[allpos,npos,file_shotpos,err]
    
def find_label(allpos,npos,file_shotpos):  # find which file name corresponds to which shot position
    filelabel=[]
    for i, val in enumerate(file_shotpos):
        for j, pos in enumerate(allpos):
            if val[0] == pos[0]: 
                filelabel.append([val[1],j+1])
                print(val, pos[0])
    return(filelabel)

def write_uni2(pat,fil,npos,allpos,filelabel,err): # write positions and artimes in uni2 formatted file for inversion
    fout = pat+fil 
    fi=open(fout, 'w')
    firstline=str(npos)+'\t'+'# total positions (geophones + shots - duplicates)\n'
    fi.write(firstline)
    secondline='#x \t y \t # label:\n'
    fi.write(secondline)
    for i, val in enumerate(allpos):
        ostra=str(val[0])+'\t'+str(val[1])+'\t'+str(i+1)+'\n'
        fi.writelines(ostra)
    fi.close()
  
    ## Add arrival times for each file, with labels of shots and geophones:
    fi = open(fout,'a')
    nreadings=0
    for i, nala in enumerate(filelabel):
        fil=open (pat+nala[0],'r'); print (nala[0])
        alines = fil.readlines()[1:]
        for j in alines:
            pp=float(j.split(',')[0])
            tt=float(j.split(',')[1])
            for k, val in enumerate(allpos):
                if pp == val[0]: 
                    newlin=str(nala[1])+'\t'+str(k+1)+'\t'+str(tt)+'\t'+str(err)+'\n'
                    fi.write(newlin)
                    nreadings=nreadings+1
    fi.close()

    ## Insert total number of picks and comment line in unified after positions list
    linum=npos+2
    with open(fout, "r+") as f:
        contents = f.readlines()
        contents.insert(linum,'# s \t g \t t\t err\n')
        adli=str(nreadings)+'\t'+'#total picks\n'
        contents.insert(linum,adli)
        f.seek(0)
        f.writelines(contents)


def on_button_clicked(_): # refresh dict.yml file contents, and perform all operations to produce uni2 file
    update_dict()
    sort_list()
    allpos,npos,file_shotpos,err=sort_list.data
    filelabel=find_label(allpos,npos,file_shotpos)
    write_uni2(fpath.value,uni2file.value,npos,allpos,filelabel,err)
    print('updated')
#

# set up the format of the input widgets:
words = ['path to files', 'average error (s)', 'file names:', 'name of project:', ' ']
items = [widgets.Label(str(i)) for i in words]
f = open('dict.yml')
data = f.read()
d = ast.literal_eval(data)
fpath    = widgets.Text(d['path'])
uni2file = widgets.Text(d['project_name'])
aerr = widgets.Text(d['error'])
# fnames = [widgets.Text(nn) for nn in d['files']]
# #
# button = widgets.Button(description='Update setup', button_style = 'danger')

# button.on_click(on_button_clicked) ############# link to action when clicked 'Update setup'
# col_1 = VBox([items[0],items[3],items[1]])
# col_2 = VBox([fpath, uni2file, aerr, items[4], items[4], items[4], button])
# col_3 = VBox([items[2]])
# col_4 = VBox(fnames)
fnames = [widgets.Text(nn) for nn in d['files']]
title2 = '1) Edit path + filenames of arrival picks, set error and project name'
label2 = widgets.Label(value = title2, style=dict(
        font_style='bold',font_family = 'Sans',font_size = '32px',
        text_color='black'
         ))
button = widgets.Button(description='Update setup', button_style = 'danger')
button.on_click(on_button_clicked) ############# link to action when clicked 'Update setup'
#
lin_0 = HBox([label2])
col_1 = VBox([items[0],items[3],items[1]])
col_2 = VBox([fpath, uni2file, aerr, items[4], items[4], items[4], button])
col_3 = VBox([items[2]])
col_4 = VBox(fnames)
#
#

