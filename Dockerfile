FROM python:3.11.2-slim

USER root

RUN apt-get update && apt-get install -y python3-opencv

RUN mkdir -p /app/examples
RUN mkdir -p /app/src
WORKDIR /app

COPY requirements.txt /app/

RUN pip install notebook==7.3.2
RUN pip install -r requirements.txt 

COPY src /app/src
COPY examples/main.ipynb /app/examples/main.ipynb

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--notebook-dir=/app/examples", "--ServerApp.allow_remote_access=True", "--ServerApp.token=''", "--no-browser"]
