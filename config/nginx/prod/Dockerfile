FROM nginx:latest

RUN mkdir /nginx

RUN apt-get update && \
    apt-get install -y \
        wget \
        gnupg2

RUN wget -O /usr/bin/certbot-auto https://dl.eff.org/certbot-auto && \
    chmod a+x /usr/bin/certbot-auto

# Create dummy self-signed certs to allow nginx to live
#RUN mkdir -p /etc/letsencrypt/live/api.billshare.io/ && \
#    openssl req -x509 -nodes -newkey rsa:4096 \
#        -keyout /etc/letsencrypt/live/api.billshare.io/privkey.pem \
#        -out /etc/letsencrypt/live/api.billshare.io/fullchain.pem \
#        -subj "/C=CA/ST=Ontario/L=Toronto/O=Billshare/CN=api.billshare.io" && \
#    wget -O /etc/letsencrypt/live/api.billshare.io/fullchain.pem "https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem"

# RUN yes | certbot-auto certonly --nginx --agree-tos --email admin@billshare.io -d api.billshare.io
# docker-compose -f docker-compose.prod.yml exec nginx bash -c 'yes | certbot-auto certonly --nginx --agree-tos --email admin@billshare.io -d api.billshare.io'

COPY letsencrypt /etc/letsencrypt/
COPY config/nginx/prod/uwsgi_params /nginx/
COPY config/nginx/prod/nginx-app.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]