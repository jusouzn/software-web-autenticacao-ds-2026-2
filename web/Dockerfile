FROM nginx:1.27-alpine

# Certificado autoassinado, suficiente para rodar localmente.
# Em produção ele seria trocado por um certificado emitido por uma CA (ex.: Let's Encrypt).
RUN apk add --no-cache openssl \
 && mkdir -p /etc/nginx/certificados \
 && openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
        -subj "/CN=localhost" \
        -addext "subjectAltName=DNS:localhost,DNS:auth.exemplo.com.br" \
        -keyout /etc/nginx/certificados/servidor.key \
        -out /etc/nginx/certificados/servidor.crt \
 && rm -rf /usr/share/nginx/html/*

COPY nginx.conf     /etc/nginx/conf.d/default.conf
COPY seguranca.conf /etc/nginx/seguranca.conf
COPY html/          /usr/share/nginx/html/
