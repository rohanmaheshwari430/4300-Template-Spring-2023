FROM python:3.7-slim

ENV CONTAINER_HOME=/var/www

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

ARG DB_NAME
ENV DB_NAME $DB_NAME

RUN pip install -r $CONTAINER_HOME/requirements.txt

# FROM node:18-alpine

# WORKDIR $CONTAINER_HOME/my-app

# ENV PATH $CONTAINER_HOME/node_modules/.bin:$PATH

# ADD /my-app .
# RUN npm ci

# RUN npm install react-scripts@5.0.1 -g --silent

# RUN npm run build

# WORKDIR $CONTAINER_HOME
