FROM node:18-alpine as build-stage

# set working directory
WORKDIR $CONTAINER_HOME

ADD . $CONTAINER_HOME

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH $CONTAINER_HOME/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json .
COPY package-lock.json .
RUN npm ci
RUN npm install react-scripts@5.0.1 -g --silent

# build app
RUN npm run build

FROM nginx:latest as production-stage
RUN mkdir /app
COPY --from=build-stage $CONTAINER_HOME/build /app
COPY nginx.conf /etc/nginx/nginx.conf