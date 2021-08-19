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
import matplotlib

import plotly.express as px
import plotly.graph_objects as go
import time as t
import altair as alt
from collections import Counter
# Initialising variables
from apps.upload import ss

import SessionState

from scipy.interpolate import splev, splrep


sc = SessionState.get(x = [])
sc = SessionState.get(y = [])
sc = SessionState.get(k = [])

#fig.patch.set_facecolor('white')
#line, = ax.plot(0, 0)
#plt.axis('scaled')
#plt.axis('off')

#@st.cache
def load_contour(i):
    exp_name = ss.dirname[3:18]
    analysis_path = 'X:\\'+exp_name
    tables_path= 'Z:\\'+exp_name
    sc.x = []
    with open(tables_path+'\\'+exp_name+'_EdgeSpline\\trace'+str(i).zfill(3)+'\\'+exp_name+'_ControlX.txt') as f:
        lines=f.readlines()
        for line in lines:
            sc.x.append(np.fromstring(line, dtype=float, sep='\t'))

    sc.y = []
    with open(tables_path+'\\'+exp_name+'_EdgeSpline\\trace'+str(i).zfill(3)+'\\'+exp_name+'_ControlY.txt') as f:
        lines=f.readlines()
        for line in lines:
            sc.y.append(np.fromstring(line, dtype=float, sep='\t'))

    sc.k = []
    with open(tables_path+'\\'+exp_name+'_EdgeSpline\\trace'+str(i).zfill(3)+'\\'+exp_name+'_Knots.txt') as f:
        lines=f.readlines()
        for line in lines:
            sc.k.append(np.fromstring(line, dtype=float, sep='\t'))

    sc.frames = []
    with open(tables_path+'\\'+exp_name+'_EdgeSpline\\trace'+str(i).zfill(3)+'\\'+exp_name+'_Frames.txt') as f:
        lines=f.readlines()
        for line in lines:
            sc.frames.append(np.fromstring(line, dtype=float, sep='\t'))

def app():

    i = st.number_input('Trajectory Number:',value = 1,min_value = 1,max_value =len(ss.area))
    load_contour(i+1)

    fig, (ax1, ax2) = plt.subplots(2,1,figsize=(6,4))
    bg = fig.canvas.copy_from_bbox(fig.bbox)

    line, = ax2.plot(0,0)
    hl, = ax1.plot(0,0,'o',markersize=1)
    the_plot = st.pyplot(plt)

    u = np.linspace(0., 1., 200)

    ax2.set_xlim(-15,15)
    ax2.set_ylim(-5,5)
    ax2.axis('off')

    first = np.where(np.isfinite(ss.area[i]))[0][0]
    last = np.where(np.isfinite(ss.area[i]))[0][-1]
    xlim_min = (ss.time[i][first]+ss.time[i][last])*.5-(ss.time[i][last]-ss.time[i][first])*.52
    xlim_max = (ss.time[i][first]+ss.time[i][last])*.5+(ss.time[i][last]-ss.time[i][first])*.52
    ylim_min = (np.nanmin(ss.area[i])+np.nanmax(ss.area[i]))*.5-(np.nanmax(ss.area[i])-np.nanmin(ss.area[i]))*.55
    ylim_max = (np.nanmin(ss.area[i])+np.nanmax(ss.area[i]))*.5+(np.nanmax(ss.area[i])-np.nanmin(ss.area[i]))*.55
    ax1.set_xlim(xlim_min,xlim_max)
    ax1.set_ylim(ylim_min,ylim_max)

    #j = st.number_input(value = 0,min_value = 0,max_value =len(sc.k) )
    while(True):
        start = t.time()
        fig.canvas.flush_events()
        hl.set_xdata([])
        hl.set_ydata([])
        ax1.scatter(ss.time[i],ss.area[i],color='b',alpha = 0.1,s=1)
        ax1.set_ylabel(r'Area ($\mu m^2$)')
        ax1.set_xlabel(r'Time (min)')
        for j in range(len(sc.k)-1):
            tck = (sc.k[j],[sc.x[j],sc.y[j]],3)
            y_plot,x_plot = splev(u, tck)

            hl.set_xdata(np.append(hl.get_xdata(), ss.time[i][round(sc.frames[j][0])]))
            hl.set_ydata(np.append(hl.get_ydata(), ss.area[i][round(sc.frames[j][0])]))
            #fig.canvas.restore_region(bg)
            #ax1.scatter(,,s=1,color='r')
            line.set_xdata(x_plot-np.mean(x_plot))
            line.set_ydata(y_plot-np.mean(y_plot))

            the_plot.pyplot(plt)

        st.write('Time elapsed: '+str(round(t.time()-start,3))+'s')
