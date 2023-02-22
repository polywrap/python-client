function patchVersion() {
  local package=$1
  local version=$2
  local depsArr=$3[@]
  local deps=("${!depsArr}")
  
  local pwd=$(echo $PWD)

  cd packages/$package
  poetry version $version
  if [ "${#deps[@]}" -ne "0" ]; then
    for dep in "${deps[@]}"; do
      poetry add $dep@$version
    done
  fi
  poetry lock
  cd $pwd
}


# Patching Verion of polywrap-msgpack
echo "Patching Version of polywrap-msgpack to $1"
patchVersion polywrap-msgpack $1

# Patching Verion of polywrap-result
echo "Patching Version of polywrap-result to $1"
patchVersion polywrap-result $1

# Patching Verion of polywrap-manifest
echo "Patching Version of polywrap-manifest to $1"
deps=(polywrap-msgpack polywrap-result)
patchVersion polywrap-manifest $1 deps

# Patching Verion of polywrap-core
echo "Patching Version of polywrap-core to $1"
deps=(polywrap-result polywrap-manifest)
patchVersion polywrap-core $1 deps

# Patching Verion of polywrap-wasm
echo "Patching Version of polywrap-wasm to $1"
deps=(polywrap-msgpack polywrap-result polywrap-manifest polywrap-core)
patchVersion polywrap-wasm $1 deps

# Patching Verion of polywrap-plugin
echo "Patching Version of polywrap-plugin to $1"
deps=(polywrap-msgpack polywrap-result polywrap-manifest polywrap-core)
patchVersion polywrap-plugin $1 deps

# Patching Verion of polywrap-uri-resolvers
echo "Patching Version of polywrap-uri-resolvers to $1"
deps=(polywrap-result polywrap-wasm polywrap-core)
patchVersion polywrap-uri-resolvers $1 deps

# Patching Verion of polywrap-client
echo "Patching Version of polywrap-client to $1"
deps=(polywrap-result polywrap-msgpack polywrap-manifest polywrap-core  polywrap-uri-resolvers)
patchVersion polywrap-client $1 deps
