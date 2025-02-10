output=$(yc container registry create --name practix 2>&1)

registry_id=$(echo "$output" | grep -oP '^\s*id:\s*\K[^ ]+')

cd images/

base_dir=$(pwd)

images=(
  "admin-panel" 
  "async-api" 
  "auth" 
  "etl" 
  "notifications/admin-panel" 
  "notifications/receiver" 
  "notifications/worker"
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
