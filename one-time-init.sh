#!/bin/sh

service_account_id=$(yc iam service-account list --format json | jq -r --arg name "practix-service-account" '.[] | select(.name == $name) | .id')
if [ -z "$service_account_id" ]; then
  yc iam service-account create --name "practix-service-account" --format json
  service_account_id=$(yc iam service-account get --name "practix-service-account" --format json | jq -r '.id')
fi

key_output=$(yc iam access-key create --service-account-name "practix-service-account" --format json)
access_key=$(echo "$key_output" | jq -r '.access_key.key_id')
secret_key=$(echo "$key_output" | jq -r '.secret')

yc resource-manager folder add-access-binding default --role container-registry.images.puller --subject "serviceAccount:$service_account_id"

if [ -z "$(yc storage bucket list --format json | jq -r --arg name "practix-bucket" '.[] | select(.name == $name) | .name')" ]; then
  yc storage bucket create --name practix-bucket
fi

yc resource-manager folder add-access-binding default --role storage.admin --subject "serviceAccount:$service_account_id"

export ACCESS_KEY="$access_key"
export SECRET_KEY="$secret_key"
export SERVICE_ACCOUNT_ID="$service_account_id"
