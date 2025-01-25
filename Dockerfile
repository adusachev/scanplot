FROM python:3.11.2-slim

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

RUN mkdir -p /app/examples
RUN mkdir -p /app/src
WORKDIR /app

COPY requirements.txt /app/

RUN pip install notebook
RUN pip install -r requirements.txt 

COPY src /app/src
COPY examples/main.ipynb /app/examples/main.ipynb

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--notebook-dir=/app/examples", "--ServerApp.allow_remote_access=True", "--ServerApp.token=''", "--no-browser"]
