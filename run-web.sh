#!/bin/bash
gunicorn -k uvicorn.workers.UvicornWorker -b :8080 -w 4 main:app --log-level info
