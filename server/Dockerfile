FROM python:3.10-slim-buster
WORKDIR /worker
COPY requirements.txt /worker
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python3 -m pip install --upgrade openai
COPY server.py /worker
# COPY openapi.yaml /worker
# COPY ai-plugin.json /worker
ENTRYPOINT ["python3"]
CMD ["server.py"]

