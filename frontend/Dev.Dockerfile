FROM node:20-alpine 

WORKDIR /josue_dir

COPY . .

RUN npm ci

EXPOSE 3000