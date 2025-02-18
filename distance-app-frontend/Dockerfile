
FROM node:18-alpine as build
WORKDIR /app


COPY package*.json /app/

RUN npm install

COPY . /app

RUN npm run build


# ------------ STAGE 2: Serve with NGINX ------------
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

# Expose the port (not strictly required by Docker, but good practice)
EXPOSE 80

# Default command for Nginx
CMD ["nginx", "-g", "daemon off;"]
    