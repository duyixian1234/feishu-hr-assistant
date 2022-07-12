#!/bin/bash
gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080 -w 4 main:app --log-level info
