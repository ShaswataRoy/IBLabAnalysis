import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import time
from multiapp import multiapp
from apps import home,upload,average,phase,contour


# Initialising variables

import SessionState


app = multiapp.MultiApp()
st.title('Experiment Analysis Webapp')

app.add_app('Home',home.app)
app.add_app('Upload',upload.app)
app.add_app('Average',average.app)
app.add_app('Phase',phase.app)
app.add_app('Contour',contour.app)

app.run()
