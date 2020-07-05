# pull official base image
FROM python:3.8.1-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV APP_USER flaskuser
ENV APP_GROUP ${APP_USER}
ENV APP_ROOT /home/${APP_USER}/web
ENV STATIC_ROOT /usr/src/app

# update container and install netcat
RUN apt-get update && apt-get install -y netcat

# create user
RUN groupadd -g 999 ${APP_GROUP} && \
    useradd -r --create-home -u 999 -g ${APP_GROUP} ${APP_USER}

# set work directory
RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

# copy project
RUN mkdir ${APP_ROOT}/app
COPY --chown=${APP_USER} ./app ${APP_ROOT}/app
RUN mkdir ${APP_ROOT}/data
COPY --chown=${APP_USER} ./data ${APP_ROOT}/data
RUN mkdir ${APP_ROOT}/migrations
COPY --chown=${APP_USER} ./migrations ${APP_ROOT}/migrations
COPY --chown=${APP_USER} wsgi.py ${APP_ROOT}
COPY --chown=${APP_USER} requirements.txt ${APP_ROOT}

# make static root
VOLUME ["${STATIC_ROOT}"]
RUN mkdir ${STATIC_ROOT}/static
COPY ./app/static ${STATIC_ROOT}/static

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

USER ${APP_USER}
EXPOSE 5000