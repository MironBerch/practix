#!/bin/sh

registry_id=$(yc container registry list --format json | jq -r '.[] | select(.name == "practix") | .id')

if [ -z "$registry_id" ]; then
  output=$(yc container registry create --name practix --secure 2>&1)
  registry_id=$(echo "$output" | grep -oP '^\s*id:\s*\K[^ ]+')
fi

yc container registry configure-docker

cd images/

base_dir=$(pwd)

images=(
  "admin-panel" 
  "async-api" 
  "auth" 
  "ugc"
)

for image in "${images[@]}"; do
  cd $image

  if [[ ! -f Dockerfile ]]
  then
    echo "No dockerfile for ${image} image found!"
    cd ..
    continue
  fi

  image_name=$(echo "$image" | sed 's/\//-/g' | sed 's/-$//')

  echo $image_name

  docker build . -t cr.yandex/$registry_id/$image_name
  docker push cr.yandex/$registry_id/$image_name

  cd "$base_dir"

  done

cd ..

export CONTAINER_REGISTRY_ID="$registry_id"
