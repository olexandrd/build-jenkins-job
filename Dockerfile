FROM python:3.8-alpine

RUN apk --no-cache add \
    python3-dev \
    gcc \
    libc-dev
RUN pip install --upgrade pip

COPY src /src
COPY build_job.py /build_job.py
COPY requirements/base.txt /requirements.txt

RUN chmod +x /build_job.py

WORKDIR /

RUN pip install -r requirements.txt

ENTRYPOINT ["/build_job.py"]