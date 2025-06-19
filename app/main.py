from fastapi import FastAPI, Depends, Path, HTTPException
from typing import Annotated
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
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


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



# Dependency function that takes item_id as input
def validate_item_id(item_id: int = Path(..., gt=0)):
    if item_id == 13:
        raise HTTPException(status_code=400, detail="Item 13 is forbidden")
    return item_id

@app.get("/items/{item_id_0}/{item_id_1}")
def read_item(validated_id_0: int = Depends(validate_item_id), validated_id_1: int = Depends(validate_item_id)):
    return {"item_id": validated_id}
