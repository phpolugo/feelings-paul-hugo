FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
COPY fonts/ /usr/share/nginx/html/fonts/
EXPOSE 80
