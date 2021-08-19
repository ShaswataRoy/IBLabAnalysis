import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import streamlit as st
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import statsmodels.api as sm
from sklearn.neighbors import LocalOutlierFactor

import glob
import re

import plotly.express as px
import plotly.graph_objects as go
import time as t
import altair as alt
from collections import Counter
# Initialising variables
from apps.upload import ss
import SessionState

@st.cache(suppress_st_warning=True)
def denoise_param(param):
    param_new = []
    for i in range(len(param)):
        y = param[i]

        Y = [[y[m]] for m in np.arange(len(y)) if np.isfinite(y[m]) and y[m]<20]

        if len(Y)==0:
            param_new.append(y)
            continue
        clf = LocalOutlierFactor(algorithm = 'kd_tree',n_neighbors=40)
        crossed = np.where(clf.fit_predict(Y)<0)[0]
        y_new = np.array(Y).reshape(1,-1)[0]

        y_new[crossed] = np.nan

        Yf = []
        j=0
        for m in np.arange(len(y)):
            if np.isfinite(y[m]) and y[m]<20:
                Yf.append(y_new[j])
                j=j+1
            else:
                Yf.append(np.nan)

        param_new.append(Yf)
    return(np.array(param_new))

def app():
    start = t.time()
    area = ss.area
    division_times = ss.division_times
    time = ss.time
    gen = ss.gen
    length = ss.length
    width_min = ss.width_min
    width_mean = ss.width_mean
    width_swarmer_max = ss.width_swarmer_max
    width_swarmer_min = ss.width_swarmer_min

    if len(width_min)>0:
        df =  {'Area':area,'Length':length,'Generation':gen,'Time':time,'Width Minimum':width_min,'Width Mean':width_min,'Width Swarmer Maximum':width_swarmer_max,'Width Swarmer Minimum':width_swarmer_min}
        units = {'Area':'$\mu m^2$','Length':'$\mu m$','Generation':'','Time':'min','Width Minimum':'$\mu m$','Width Mean':'$\mu m$','Width Swarmer Minimum':'$\mu m$','Width Swarmer Maximum':'$\mu m$'}

    else:
        df =  {'Area':area,'Length':length,'Generation':gen,'Time':time}
        units = {'Area':'$\mu m^2$','Length':'$\mu m$','Generation':'','Time':'min'}
    #Select Plotting Parameter
    select = st.sidebar.selectbox('Select Parameter',list(df.keys()))
    param = df[select]

    traj_range = st.sidebar.slider('Select a range of values',0, len(area), (0,5))
    y_min =  float(st.sidebar.text_input('y min',value='0.'))
    y_max =  float(st.sidebar.text_input('y max',value='20.'))
    fig = plt.figure(figsize=(15,4))

    colors = cm.viridis(np.linspace(0, 1, traj_range[1]-traj_range[0]))

    # Cell Death Filter

    denoise = st.sidebar.checkbox('Filter Noise')

    if denoise:
        param = denoise_param(param)

    death = st.sidebar.checkbox('Filter Deaths')

    if death:
        if len(ss.limits_death)==0:
            st.write("Compute Cell Deaths first")
            st.stop()
        limits = ss.limits_death[traj_range[0]:traj_range[1]]
    else:
        limits = np.tile([0,len(time[0])],(traj_range[1]-traj_range[0],1))
    for i in range(traj_range[0],traj_range[1]):
        j = i-traj_range[0]
        plt.scatter(time[i][limits[j][0]:limits[j][1]],param[i][limits[j][0]:limits[j][1]],s=10,alpha=1./(traj_range[1]-traj_range[0]),color=colors[i-traj_range[0 ]])


        # Plot Mean and Standard Deviation

    mean = st.sidebar.checkbox('Mean')
    if mean:
        lowess_mean = sm.nonparametric.lowess(np.nanmean(param,0), time[0], frac=0.0)
        plt.plot(lowess_mean[:, 0], lowess_mean[:, 1],linewidth=2,color='k')

    std = st.sidebar.checkbox('Standard Deviation')
    if std:
        lowess_std = sm.nonparametric.lowess(np.nanstd(param,0), time[0], frac=0.02)
        if not mean:
            lowess_mean = sm.nonparametric.lowess(np.nanmean(param,0), time[0], frac=0.0)
        plt.fill_between(lowess_mean[:, 0], lowess_mean[:, 1]-lowess_std[:, 1],
        lowess_mean[:, 1]+lowess_std[:, 1],linewidth=2,color='k',alpha=0.3)

    #plt.axvspan(0,60*12, alpha=0.2, color='white',label = 'PYE')

    #plt.axvspan(60*12, 60*16, alpha=0.2, color='orange',label = 'A22')
    plt.xlim(0,np.nanmax(time[0]))
    plt.ylim(y_min,y_max)
    plt.xlabel('Time ('+units['Time']+')')
    plt.ylabel(select+' ('+units[select]+')')

    st.pyplot(fig)
    st.write('Time elapsed: '+str(round(t.time()-start,3))+'s')
