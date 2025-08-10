#!/bin/bash

set -a
source .env
set +a

DOMAIN=$(echo "$DOMAIN" | tr -d '\n\r' | xargs)
SERVICE_HOST_NAME=$(echo "$SERVICE_HOST_NAME" | tr -d '\n\r' | xargs)
SERVICE_PORT=$(echo "$SERVICE_PORT" | tr -d '\n\r' | xargs)

# Debug
echo "DOMAIN: '$DOMAIN'"
echo "SERVICE_HOST_NAME: '$SERVICE_HOST_NAME'"
echo "SERVICE_PORT: '$SERVICE_PORT'"

# generate config
envsubst '$DOMAIN $SERVICE_HOST_NAME $SERVICE_PORT' < nginx/template/https.conf.template > nginx/conf.d/default.conf

echo "Generated default.conf:"
cat nginx/conf.d/default.conf