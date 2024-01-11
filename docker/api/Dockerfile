FROM python:3.11-slim

WORKDIR /workspace

# Python dependencies
COPY ./requirements.txt .
RUN pip install -U pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install uvicorn
