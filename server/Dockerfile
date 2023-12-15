FROM python:3.9.16
WORKDIR /worker
COPY requirements.txt /worker
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python3 -m pip install --upgrade openai
COPY webhook_cert.pem /worker
COPY webhook_pkey.pem /worker
COPY server.py /worker
# CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "4714"]
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "4714", "--ssl-keyfile=webhook_pkey.pem", "--ssl-certfile=webhook_cert.pem"]