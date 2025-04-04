#!/bin/sh

cd terraform/infra/

yc iam key create \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --folder-name default \
  --output key.json

terraform init -backend-config="access_key=$ACCESS_KEY" -backend-config="secret_key=$SECRET_KEY"
terraform apply -auto-approve
terraform output | tee "../../output.txt"

cd ../../

eval "$(grep 'external_cluster_cmd_str =' "output.txt" | cut -d'=' -f2 | tr -d '"') --force"

kubectl cluster-info

helm pull oci://cr.yandex/yc-marketplace/yandex-cloud/ingress-nginx/chart/ingress-nginx \
   --version 4.10.0 \
   --untar && \
helm install \
   --create-namespace \
   ingress-nginx ./ingress-nginx/
