# joinByString is a utility function to join an array of strings with a separator string
function joinByString() {
  local separator="$1"
  shift
  local first="$1"
  shift
  printf "%s" "$first" "${@/#/$separator}"
}

# isPackagePublished is a utility function to check if a package is published
# This will only work for the latest version of the package
# Can only be called inside the top level function since directory needs to be changed
function isPackagePublished() {
  local package=$1
  local version=$2

  poetry search $package | grep "$package ($version)"
  local exit_code=$?

  if [ "$exit_code" -eq "0" ]; then
    return 0
  else
    return 1
  fi
}

function patchVersion() {
  local package=$1
  local version=$2
  if [ -z "$3" ]; then
    local deps=()
  else
    local depsArr=$3[@]
    local deps=("${!depsArr}")
  fi

  echo "deps: ${deps[@]}"
  
  local pwd=$(echo $PWD)

  cd packages/$package

  poetry version $version
  local bumpVersionResult=$?
  if [ "$bumpVersionResult" -ne "0" ]; then
    echo "Failed to bump version of $package to $version"
    cd $pwd
    return 1
  fi

  if [ "${#deps[@]}" -ne "0" ]; then  # -ne is integer inequality
    if [ "${deps[0]}" != "" ]; then  # != is string inequality
      patchedDeps="$(joinByString "@$version " "${deps[@]}")@$version"
      poetry add $patchedDeps
      local addDepsResult=$?
      if [ "$addDepsResult" -ne "0" ]; then
        echo "Failed to add $patchedDeps to $package"
        cd $pwd
        return 1
      fi
    fi
  fi

  poetry lock
  local lockResult=$?
  if [ "$lockResult" -ne "0" ]; then
    echo "Failed to lock $package"
    cd $pwd
    return 1
  fi

  poetry install --no-root
  local installResult=$?
  if [ "$installResult" -ne "0" ]; then
    echo "Failed to install $package"
    cd $pwd
    return 1
  fi

  cd $pwd
}

function publishPackage() {
  local package=$1
  local version=$2
  local username=$3
  local password=$4

  local pwd=$(echo $PWD)

  cd packages/$package

  isPackagePublished $package $version
  local isPackagePublishedResult=$?
  if [ "$isPackagePublishedResult" -eq "0" ]; then
    echo "Skip publish: Package $package with version $version is already published"
    cd $pwd
    return 0
  fi

  poetry publish --build --username $username --password $password
  local publishResult=$?
  if [ "$publishResult" -ne "0" ]; then
    echo "Failed to publish $package"
    cd $pwd
    return 1
  fi

  cd $pwd
}

function waitForPackagePublish() {
  local package=$1
  local version=$2
  local seconds=0

  local pwd=$(echo $PWD)

  cd packages/$package

  while [ "$seconds" -lt "600" ] # Wait for 10 minutes
  do
    isPackagePublished $package $version
    local exit_code=$?

    if [ "$exit_code" -eq "0" ]; then
      echo "Package $package with version $version is published"
      break
    fi
    sleep 5
    seconds=$((seconds+5))
    echo "Waiting for $seconds seconds for the $package to be published"
  done

  cd $pwd

  if [ "$seconds" -eq "600" ]; then
    echo "Package $package with version $version is not published"
    return 1
  fi
}

# Patching Version of polywrap-msgpack
echo "Patching Version of polywrap-msgpack to $1"
patchVersion polywrap-msgpack $1
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-msgpack to $1"
  exit 1
fi

echo "Publishing polywrap-msgpack"
publishPackage polywrap-msgpack $1 $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-msgpack"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-msgpack $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-msgpack"
  exit 1
fi

# Patching Version of polywrap-manifest
echo "Patching Version of polywrap-manifest to $1"
deps=(polywrap-msgpack)
patchVersion polywrap-manifest $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-manifest to $1"
  exit 1
fi

echo "Publishing polywrap-manifest"
publishPackage polywrap-manifest $1 $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-manifest"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-manifest $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-manifest"
  exit 1
fi

# Patching Version of polywrap-core
echo "Patching Version of polywrap-core to $1"
deps=(polywrap-manifest polywrap-msgpack)
patchVersion polywrap-core $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-core to $1"
  exit 1
fi

echo "Publishing polywrap-core"
publishPackage polywrap-core $1 $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-core"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-core $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-core"
  exit 1
fi

# Patching Version of polywrap-wasm
echo "Patching Version of polywrap-wasm to $1"
deps=(polywrap-msgpack polywrap-manifest polywrap-core)
patchVersion polywrap-wasm $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-wasm to $1"
  exit 1
fi

echo "Publishing polywrap-wasm"
publishPackage polywrap-wasm $1 $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-wasm"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-wasm $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-wasm"
  exit 1
fi

# Patching Version of polywrap-plugin
echo "Patching Version of polywrap-plugin to $1"
deps=(polywrap-msgpack polywrap-manifest polywrap-core)
patchVersion polywrap-plugin $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-plugin to $1"
  exit 1
fi

echo "Publishing polywrap-plugin"
publishPackage polywrap-plugin $1 $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-plugin"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-plugin $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-plugin"
  exit 1
fi

# Patching Version of polywrap-uri-resolvers
echo "Patching Version of polywrap-uri-resolvers to $1"
deps=(polywrap-wasm polywrap-core)
patchVersion polywrap-uri-resolvers $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-uri-resolvers to $1"
  exit 1
fi

echo "Publishing polywrap-uri-resolvers"
publishPackage polywrap-uri-resolvers $1 $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-uri-resolvers"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-uri-resolvers $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-uri-resolvers"
  exit 1
fi

# Patching Version of polywrap-client-config-builder
echo "Patching Version of polywrap-client-config-builder to $1"
deps=(polywrap-core polywrap-uri-resolvers)
patchVersion polywrap-client-config-builder $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-client-config-builder to $1"
  exit 1
fi

echo "Publishing polywrap-client-config-builder"
publishPackage polywrap-client-config-builder $1 $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-client-config-builder"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-client-config-builder $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-client-config-builder"
  exit 1
fi

# Patching Version of polywrap-client
echo "Patching Version of polywrap-client to $1"
deps=(polywrap-msgpack polywrap-manifest polywrap-core  polywrap-uri-resolvers)
patchVersion polywrap-client $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-client to $1"
  exit 1
fi

echo "Publishing polywrap-client"
publishPackage polywrap-client $1 $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-client"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-client $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-client"
  exit 1
fi
