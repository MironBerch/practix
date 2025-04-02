#!/bin/sh

cd terraform/k8s/

terraform init
terraform apply \
  -var="iam_access_key=$ACCESS_KEY" \
  -var="iam_secret_key=$SECRET_KEY" \
  -var="container_registry_id=$CONTAINER_REGISTRY_ID" \
  -auto-approve

cd ../..
