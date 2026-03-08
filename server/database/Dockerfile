FROM node:18.12.1-bullseye-slim

WORKDIR /usr/src/app
COPY package*.json ./

RUN npm install -g npm@9.1.3

ADD package.json .
ADD app.js .
ADD review.js .
ADD dealership.js .
ADD data/dealerships.json .
ADD data/reviews.json .
COPY . .
RUN npm install

EXPOSE 3030

CMD [ "node", "app.js" ]
