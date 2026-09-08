FROM nginx:alpine
COPY index.html favicon.ico favicon-16.png favicon-32.png apple-touch-icon.png /usr/share/nginx/html/
# robots.txt porte Disallow: / — le mémoire se partage par lien, il n'a pas à
# être trouvable dans un moteur de recherche.
COPY robots.txt memoire.pdf /usr/share/nginx/html/
COPY fonts/ /usr/share/nginx/html/fonts/
EXPOSE 80
