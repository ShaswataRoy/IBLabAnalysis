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
import glob
import re
from apps.average import denoise_param

import plotly.express as px
import plotly.graph_objects as go
import time as t
import altair as alt
from collections import Counter
# Initialising variables
from apps.upload import ss

import SessionState

def plot_param(x):
    y =  sm.nonparametric.lowess(np.nanmean(x,axis=0), np.linspace(0,1,100), frac=0)
    M_new_vec = np.nanmean(x,axis=0)
    Sigma_new_vec = np.nanstd(x,axis=0)

    lower_bound = M_new_vec - Sigma_new_vec
    upper_bound = M_new_vec + Sigma_new_vec

    lb = sm.nonparametric.lowess(lower_bound, np.linspace(0,1,100), frac=0)
    ub = sm.nonparametric.lowess(upper_bound, np.linspace(0,1,100), frac=0)

    return(y,lb,ub)

def app():
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

    denoise = st.sidebar.checkbox('Filter Noise')

    if denoise:
        param = denoise_param(param)

    param_h = []
    for j in range(len(gen)):
        gen1 = np.nan_to_num(gen[j])
        division_times = np.where(gen1[1:]-gen1[:-1]>0.5)[0]
        division_times = [t for t in division_times]
        for i in range(len(division_times)-2):
            param_h.append(list(zip(np.linspace(0,1,division_times[i+1]-division_times[i]-1),param[j][division_times[i]+1:division_times[i+1]])))
    param_init = []
    for i in range(300):
        param_init.append(np.interp(np.linspace(0,1,100),list(zip(*param_h[i]))[0][1:],list(zip(*param_h[i]))[1][1:]))

    param_m,param_l,param_u = plot_param(param_init)

    log_scale = st.sidebar.checkbox('Log')
    y_min =  float(st.sidebar.text_input('y min',value=str(round(np.min(param_l[:,1]),3))))
    y_max =  float(st.sidebar.text_input('y max',value=str(round(np.max(param_u[:,1]),3))))

    fig = plt.figure(figsize=(4,4),dpi=400)

    plt.plot(param_m[:, 0], param_m[:, 1])
    plt.fill_between(np.linspace(0,1,100), param_l[:,1], param_u[:,1], alpha=.2)

    plt.xlabel('$\phi$',fontsize=10)
    plt.ylabel(select+' ('+units[select]+')',fontsize=10,rotation=90,labelpad=20)
    if log_scale:
        plt.yscale('log')
    plt.legend(loc =2)
    plt.xlim(0,1)
    plt.ylim(y_min,y_max)
    st.pyplot(fig)
