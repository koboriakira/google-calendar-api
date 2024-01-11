#!/bin/bash

cd /workspace/gc_api && uvicorn main:app --reload --port=8080 --host=0.0.0.0
