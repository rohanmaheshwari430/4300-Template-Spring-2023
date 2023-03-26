FROM node:18-alpine

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

# start app
CMD ["npm", "start"]