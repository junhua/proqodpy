# FROM django:python2-onbuild
FROM python:2-onbuild

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
