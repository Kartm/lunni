# Stage 0, build and compile the frontend
FROM node:14.14.0-alpine as build-stage
WORKDIR /app
COPY ./package.json ./
RUN npm i
COPY . ./
RUN npm run build

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx
COPY --from=build-stage /app/build/ /usr/share/nginx/html
# Copy the default nginx.conf provided by tiangolo/node-frontend
COPY --from=build-stage /app/nginx.conf /etc/nginx/conf.d/default.conf