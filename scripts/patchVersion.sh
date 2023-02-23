function patchVersion() {
  local package=$1
  local version=$2
  if [ -z "$3" ]; then
    local deps=()
  else
    local depsArr=$3[@]
    local deps=("${!depsArr}")
  fi
  
  local pwd=$(echo $PWD)

  cd packages/$package
  echo "Patching $package to version $version"
  poetry version $version
  if [ "${#deps[@]}" -ne "0" ]; then
    if [ "${deps[0]}" != "" ]; then
      for dep in "${deps[@]}"; do
        poetry add $dep@$version
      done
    fi
  fi
  poetry lock
  poetry install
  cd $pwd
}

function publishPackage() {
  local package=$1
  local username=$2
  local password=$3

  local pwd=$(echo $PWD)

  cd packages/$package
  poetry version
  poetry publish --build --username $username --password $password
  cd $pwd
}


# Patching Verion of polywrap-msgpack
echo "Patching Version of polywrap-msgpack to $1"
patchVersion polywrap-msgpack $1
echo "Publishing polywrap-msgpack"
publishPackage polywrap-msgpack $2 $3

# Patching Verion of polywrap-result
echo "Patching Version of polywrap-result to $1"
patchVersion polywrap-result $1
echo "Publishing polywrap-result"
publishPackage polywrap-result $2 $3

# Patching Verion of polywrap-manifest
echo "Patching Version of polywrap-manifest to $1"
deps=(polywrap-msgpack polywrap-result)
patchVersion polywrap-manifest $1 deps
echo "Publishing polywrap-manifest"
publishPackage polywrap-manifest $2 $3

# Patching Verion of polywrap-core
echo "Patching Version of polywrap-core to $1"
deps=(polywrap-result polywrap-manifest)
patchVersion polywrap-core $1 deps
echo "Publishing polywrap-core"
publishPackage polywrap-core $2 $3

# Patching Verion of polywrap-wasm
echo "Patching Version of polywrap-wasm to $1"
deps=(polywrap-msgpack polywrap-result polywrap-manifest polywrap-core)
patchVersion polywrap-wasm $1 deps
echo "Publishing polywrap-wasm"
publishPackage polywrap-wasm $2 $3

# Patching Verion of polywrap-plugin
echo "Patching Version of polywrap-plugin to $1"
deps=(polywrap-msgpack polywrap-result polywrap-manifest polywrap-core)
patchVersion polywrap-plugin $1 deps
echo "Publishing polywrap-plugin"
publishPackage polywrap-plugin $2 $3

# Patching Verion of polywrap-uri-resolvers
echo "Patching Version of polywrap-uri-resolvers to $1"
deps=(polywrap-result polywrap-wasm polywrap-core)
patchVersion polywrap-uri-resolvers $1 deps
echo "Publishing polywrap-uri-resolvers"
publishPackage polywrap-uri-resolvers $2 $3

# Patching Verion of polywrap-client
echo "Patching Version of polywrap-client to $1"
deps=(polywrap-result polywrap-msgpack polywrap-manifest polywrap-core  polywrap-uri-resolvers)
patchVersion polywrap-client $1 deps
echo "Publishing polywrap-client"
publishPackage polywrap-client $2 $3
