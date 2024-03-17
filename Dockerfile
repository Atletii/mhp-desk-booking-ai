FROM python:3.10-slim-buster

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install libgl1 libglib2.0-0 -y
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libgomp.so.1

# Install app dependencies
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
