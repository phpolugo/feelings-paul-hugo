FROM nginx:alpine
COPY index.html favicon.ico favicon-16.png favicon-32.png apple-touch-icon.png /usr/share/nginx/html/
COPY fonts/ /usr/share/nginx/html/fonts/
EXPOSE 80
