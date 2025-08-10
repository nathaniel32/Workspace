rem start app
docker-compose up -d workspace_db workspace_app

rem start http-server
docker-compose run --rm nginx-http-config
docker-compose up -d nginx

rem make ssl
rem docker run --rm -it -v ${PWD}/nginx/certbot/conf:/etc/letsencrypt -v ${PWD}/nginx/certbot/www:/var/www/certbot certbot/certbot certonly --webroot --webroot-path=/var/www/certbot --email your-email@domain.com --agree-tos --no-eff-email -d belikucing.com -d www.belikucing.com
docker-compose run --rm certbot-init

rem start https-server
docker-compose run --rm nginx-https-config
docker-compose down nginx
docker-compose up -d nginx

rem auto renew
docker-compose up -d certbot