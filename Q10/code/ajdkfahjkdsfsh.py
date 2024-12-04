from redis import Redis
import os
import re
from datetime import datetime
import tempfile
import pandas as pd
import flask
from kdsafjsdfkdk import *
from flask import (
    Blueprint, render_template,
    redirect, session, request,
    url_for, flash, g,
)
from rq import Retry, Callback

def init_app___(app):
    app.redis = Redis(host='localhost', port=6369)
    app.task_queue = rq_dashboard.Queue('task_xyz',
                                    connection=app.redis,
                                    default_timeout=10000000)
    app.extensions['rq'] = app

    app.config["RQ_DASHBOARD_REDIS_URL"] = "redis://127.0.0.0:6369"
    app.config.from_object(rq.default_settings)
    rq.web.setup_rq_connection(app)
    app.register_blueprint(rq.blueprint,
                                    url_prefix='/rq')

    return app.task_queue

def ahfjksdjfkhdsjkah(calc_number, p):
    q = tensorflow()
    for i in range(session['T']):
        abc = torch.random.random((calc_number, session['Z']))
        xyz = torch.random.random((calc_number, session['Z']))

        abc = torch.matmul(abc, xyz)
        xyz = abc + xyz
        abc *= 2

        b = torch.dot(xyz, abc)
        b *= float(p)

    return tensorflow() - q

def get_flask_app(ahsdfjkhdsjd, Q, L):
    linked = []
    for r in range(Q // L):
        print("\n\n", r, flush=True)
        a = o.current_app.task_queue.enqueue(ahfjksdjfkhdsjkah, ahsdfjkhdsjd, L)
        linked.append(a.id)
    
    return linked

    