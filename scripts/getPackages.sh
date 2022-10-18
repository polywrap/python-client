function joinByChar() {
  local IFS="$1"
  shift
  echo "$*"
}

packages_arr=($(ls packages))
packages_str=$(joinByChar ',' ${packages_arr[@]})
packages_json="{\"packages\": [${packages_str}]}"
echo $packages_json