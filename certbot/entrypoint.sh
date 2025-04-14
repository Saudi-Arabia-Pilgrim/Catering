#!/bin/bash
set -e

# Default values
DOMAIN=${DOMAIN:-api.catering.mukhsin.space}
CERT_EMAIL=${CERT_EMAIL:-muxsinmuxtorov01@gmail.com}
RSA_KEY_SIZE=${RSA_KEY_SIZE:-4096}
STAGING=${STAGING:-0} # Set to 1 for testing

# Create a self-signed certificate for the first run
if [ ! -d "/etc/letsencrypt/live/$DOMAIN" ]; then
  echo "### Creating self-signed certificate for first run"
  mkdir -p /etc/letsencrypt/live/$DOMAIN
  openssl req -x509 -nodes -newkey rsa:$RSA_KEY_SIZE -days 1 \
    -keyout "/etc/letsencrypt/live/$DOMAIN/privkey.pem" \
    -out "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" \
    -subj "/CN=$DOMAIN"
fi

# Function to reload Nginx
reload_nginx() {
  echo "### Reloading Nginx configuration"
  curl --silent --fail -X POST http://nginx:80/reload || true
}

# Function to request/renew certificate
request_certificate() {
  echo "### Requesting Let's Encrypt certificate for $DOMAIN"
  
  # Select appropriate options based on staging flag
  staging_arg=""
  if [ $STAGING -eq 1 ]; then
    staging_arg="--staging"
  fi
  
  # Request the certificate
  certbot certonly --webroot -w /var/www/catering.mukhsin.space \
    $staging_arg \
    --email $CERT_EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    --rsa-key-size $RSA_KEY_SIZE \
    --force-renewal
    
  # Reload Nginx to apply the new certificate
  reload_nginx
}

# Initial certificate request
request_certificate

# Set up the renewal cron job
echo "### Setting up certificate renewal cron job"
echo "0 */12 * * * certbot renew --quiet --deploy-hook 'curl --silent --fail -X POST http://nginx:80/reload || true'" > /etc/crontabs/root

# Keep the container running
echo "### Certificate obtained successfully. Certbot container is now running in the background."
exec crond -f