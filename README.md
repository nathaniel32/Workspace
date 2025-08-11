## Workspace

### start app
docker-compose up -d workspace_db workspace_app

### start http-server
docker-compose run --rm nginx-http-config
docker-compose up -d nginx

### make ssl
docker-compose run --rm certbot-init

### start https-server
docker-compose run --rm nginx-https-config
docker-compose down nginx
docker-compose up -d nginx

### auto renew
docker-compose up -d certbot