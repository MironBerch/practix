#!/bin/sh

cd terraform/k8s/

terraform init
terraform apply -auto-approve
