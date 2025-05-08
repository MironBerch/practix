#!/bin/sh

cd images/

base_dir=$(pwd)

images=(
  "admin-panel" 
  "async-api" 
  "auth" 
  "etl/postgres-to-elastic"
  "etl/postgres-to-mongo" 
  "notifications/admin-panel" 
  "notifications/receiver" 
  "notifications/worker"
  "ugc"
)

for image in "${images[@]}"; do
  cd $image

  image_name=$(echo "$image" | sed 's/\//-/g' | sed 's/-$//')

  echo $image_name

  flake8 .
  isort .
  black .

  cd "$base_dir"

  done

cd ..
