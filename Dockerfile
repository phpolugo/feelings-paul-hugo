FROM nginx:alpine
COPY index.html favicon.ico favicon-16.png favicon-32.png apple-touch-icon.png /usr/share/nginx/html/
# robots.txt porte Disallow: / — le mémoire se partage par lien, il n'a pas à
# être trouvable dans un moteur de recherche.
COPY robots.txt memoire.pdf /usr/share/nginx/html/
# /memoire/ : la page du mémoire, pour l'entourage. La racine reste la page
# bande-son, celle que le QR code du PDF promet à ses lecteurs.
COPY memoire/ /usr/share/nginx/html/memoire/
COPY fonts/ /usr/share/nginx/html/fonts/
EXPOSE 80
