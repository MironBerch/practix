#!/bin/sh

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

  image_name=$(echo "$image" | sed 's/\//-/g' | sed 's/-$//')

  echo $image_name

  uv run flake8 .
  uv run isort .
  uv run black .
  uv run mypy .

  cd "$base_dir"

  done

cd ..
