from fastapi import FastAPI
import json
import datetime as dt
from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.io import curdoc
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from models import TimeseriesArgs

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
curdoc().theme = 'dark_minimal'

@app.get('/')
def root():
    return True

@app.post('/plot')
def get_plot(args: TimeseriesArgs):
    p = figure(width=600, height=300, x_axis_type="datetime")
    x = [dt.datetime.fromisoformat(time) for time in args.times]
    y = args.data
    y_axis_label = f"{args.variable} [{args.units}]"
    p.scatter(x, y)
    p.xaxis.axis_label = 'time'
    p.yaxis.axis_label = y_axis_label
    j = json_item(p, 'bk-plot', theme='dark_minimal')
    return j
