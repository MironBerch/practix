#!/bin/sh

cd images/

base_dir=$(pwd)

images=("admin-panel")
go_images=(
  "ugc" 
  "async-api" 
  "auth"
)

for image in "${images[@]}"; do
  cd $image

  image_name=$(echo "$image" | sed 's/\//-/g' | sed 's/-$//')

  echo $image_name

  sudo rm -r .venv
  uv run flake8 .
  uv run isort .
  uv run black .
  uv run mypy .

  cd "$base_dir"

  done

for image in "${go_images[@]}"; do
  cd $image

  image_name=$(echo "$image" | sed 's/\//-/g' | sed 's/-$//')

  echo $image_name

  gofmt -w .
  go fmt ./...

  cd "$base_dir"

  done

cd ..
