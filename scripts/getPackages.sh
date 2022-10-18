function joinByString() {
  local separator="$1"
  shift
  local first="$1"
  shift
  printf "%s" "$first" "${@/#/$separator}"
}

packages_arr=($(ls packages))
packages_str=$(joinByString ', ' ${packages_arr[@]})
packages_json="{ \"packages\": [ ${packages_str} ] }"
echo $packages_json