# pull official base image
FROM python:3.8.0-alpine

# Define requirements file
ARG requirements=requirements/development.txt

# Define settings file
ENV DJANGO_SETTINGS_MODULE=cmux_project.settings.development

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 and temporary Pillow dependencies
RUN apk update \
    && apk add --virtual build-deps jpeg-dev \
    && apk add gcc python3-dev musl-dev \
    && apk add postgresql-dev gettext \
    && apk add zlib-dev libjpeg

# upgrade pip and install requirements
RUN pip install --upgrade pip
COPY requirements/ /usr/src/app/requirements/
RUN pip install -r $requirements

# remove Pillow dependencies
RUN apk del build-deps

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]