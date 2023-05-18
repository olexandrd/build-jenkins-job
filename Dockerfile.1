FROM python:3.8-alpine

COPY src /src
COPY build_job.py /build_job.py
COPY requirements/base.txt /requirements.txt

RUN chmod +x /build_job.py

WORKDIR /
RUN apk --no-cache add \
    python3-dev \
    gcc \
    libc-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del -r \
    python3-dev \
    gcc \
    libc-dev

ENTRYPOINT ["/build_job.py"]