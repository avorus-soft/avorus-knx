FROM python:3.11-slim

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir --upgrade \
	asyncclick==8.1.3.4 \
	anyio==3.6.2 \
	requests==2.30.0 \
	aiomqtt==1.1.0 \
	xknx==2.11.2
