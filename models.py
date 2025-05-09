from pydantic import BaseModel
from typing import List

class TimeseriesArgs(BaseModel):
    times: List
    data: List
    variable: str
    units: str
