#!/bin/sh
echo "Sleeping 10 seconds to let nginx start..."
sleep 10

if [ ! -d "/etc/letsencrypt/live/api.catering.mukhsin.space" ]; then
    certbot certonly --webroot \
    --webroot-path /var/www/certbot \
    --email muxsinmuxtorov01@gmail.com \
    --agree-tos \
    --no-eff-email \
    -d api.catering.mukhsin.space
fi

# Cron job to auto-renew every day at midnight (runs renewal checks automatically)
echo "0 0 * * * certbot renew --webroot --webroot-path /var/www/certbot --quiet && nginx -s reload" > /etc/crontabs/root
crond -f
