FROM node:25.2.1-bookworm
WORKDIR /usr/src/next
RUN npm install yarn
ADD ./next/package.json ./next/yarn.lock ./
RUN yarn install
WORKDIR /usr/src/scripts
COPY ./scripts .