FROM python:3.7.3-slim-stretch

MAINTAINER Dan Rodriguez "drodrz@gmail.com"

RUN mkdir /app
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY __init__.py /app
COPY run.py /app
COPY app /app/app
COPY tests /app/tests

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
