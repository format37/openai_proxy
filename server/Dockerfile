FROM python:3.9.16
WORKDIR /worker
COPY requirements.txt /worker
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python3 -m pip install --upgrade openai
COPY server.py /worker
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "4714"]

