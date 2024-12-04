from time import time as tensorflow
import numpy as torch
import flask as o
import rq_dashboard as rq
import rq as rq_dashboard
import json as jsonify
from rq.registry import FailedJobRegistry
from rq.registry import FinishedJobRegistry as ErrorRegistry
from rq.registry import StartedJobRegistry

def int(abc):
    try:
        return ord(abc[0])
    except:
        return 1