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

import plotly.express as px
import plotly.graph_objects as go
import time as t
import altair as alt
from collections import Counter
# Initialising variables

import SessionState


ss = SessionState.get(dirname="Z:/2021-03-03-1301")
ss = SessionState.get(limits_death = [])
ss = SessionState.get(area = [])
ss = SessionState.get(division_times = [])
ss = SessionState.get(gen = [])
ss = SessionState.get(time = [])
ss = SessionState.get(length = [])
ss = SessionState.get(width_min = [])
ss = SessionState.get(width_mean = [])
ss = SessionState.get(width_swarmer_max = [])
ss = SessionState.get(width_swarmer_min = [])


def initialise():
    plt.style.use('science')
    root = tk.Tk()
    root.withdraw()

    root.wm_attributes('-topmost', 1)

    st.title('Select Experiment')
    st.write('Select a Table:')
    clicked = st.button('Choose')
    if clicked:
        ss.dirname = filedialog.askdirectory(master=root)
        st.text_input('Selected experiment:', ss.dirname[3:18])

@st.cache(persist=True)
def load_variables(dirname):
    area = []
    division_times = []
    time = []
    gen = []
    length = []
    width_min = []
    width_mean = []
    width_swarmer_max = []
    width_swarmer_min = []


    files = glob.glob(dirname+'/*')

    area_file = list(filter(re.compile(".*_Area.txt").match, files))[0]
    div_file = list(filter(re.compile(".*_DivisionTime.txt").match, files))[0]
    time_file = list(filter(re.compile(".*_Time.txt").match, files))[0]
    gen_file = list(filter(re.compile(".*_Generation.txt").match, files))[0]
    length_file = list(filter(re.compile(".*_Length.txt").match, files))[0]

    shape_exist =  list(filter(re.compile(".*_WidthMin.txt").match, files))
    if len(shape_exist)>0:
        width_min_file = list(filter(re.compile(".*_WidthMin.txt").match, files))[0]
        width_mean_file = list(filter(re.compile(".*_WidthMean.txt").match, files))[0]
        width_swarmer_max_file = list(filter(re.compile(".*_WidthSwarmerMax.txt").match, files))[0]
        width_swarmer_min_file = list(filter(re.compile(".*_WidthSwarmerMin.txt").match, files))[0]

        with open(width_min_file) as f:
            lines=f.readlines()
            for line in lines:
                width_min.append(np.fromstring(line, dtype=float, sep='\t'))

        with open(width_mean_file) as f:
            lines=f.readlines()
            for line in lines:
                width_mean.append(np.fromstring(line, dtype=float, sep='\t'))

        with open(width_swarmer_max_file) as f:
            lines=f.readlines()
            for line in lines:
                width_swarmer_max.append(np.fromstring(line, dtype=float, sep='\t'))

        with open(width_swarmer_min_file) as f:
            lines=f.readlines()
            for line in lines:
                width_swarmer_min.append(np.fromstring(line, dtype=float, sep='\t'))



    with open(area_file) as f:
        lines=f.readlines()
        for line in lines:
            area.append(np.fromstring(line, dtype=float, sep='\t'))

    with open(div_file) as f:
        lines=f.readlines()
        for line in lines:
            division_times.append(np.fromstring(line, dtype=float, sep='\t'))

    with open(time_file) as f:
        lines=f.readlines()
        for line in lines:
            time.append(np.fromstring(line, dtype=float, sep='\t'))

    with open(gen_file) as f:
        lines=f.readlines()
        for line in lines:
            gen.append(np.fromstring(line, dtype=float, sep='\t'))

    with open(length_file) as f:
        lines=f.readlines()
        for line in lines:
            length.append(np.fromstring(line, dtype=float, sep='\t'))

    return area,division_times,time,gen,length,width_mean,width_min,width_swarmer_max,width_swarmer_min

@st.cache(suppress_st_warning=True)
def filter_traj(min,max,gen):
    limits = []
    progress_bar = st.progress(0)

    for i in range(min,max):
        last = pd.DataFrame(gen[i].T).apply(pd.Series.last_valid_index)[0]
        for c in Counter(gen[i]).items():
            if c[1]>200:
                last = np.argwhere(gen[i] == c[0])[0][0]-1
                break

        first = pd.DataFrame(gen[i].T).apply(pd.Series.first_valid_index)[0]
        limits.append([first,last])
        progress_bar.progress((i + 1)*1./(max-min))
    return limits

def app():
    start = t.time()
    initialise()
    ss.area,ss.division_times,ss.time,ss.gen,ss.length,ss.width_min,ss.width_mean,ss.width_swarmer_max,ss.width_swarmer_min = load_variables(ss.dirname)

    compute = st.button('Compute Deaths')
    if compute:
        ss.limits_death = filter_traj(0,len(ss.area),ss.gen)

    st.write('Time elapsed: '+str(round(t.time()-start,3))+'s')
