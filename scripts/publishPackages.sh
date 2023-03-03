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
    return 1
  fi

  if [ "${#deps[@]}" -ne "0" ]; then  # -ne is integer inequality
    if [ "${deps[0]}" != "" ]; then  # != is string inequality
      for dep in "${deps[@]}"; do
        poetry add $dep@$version
        local addDepResult=$?
        if [ "$addDepResult" -ne "0" ]; then
          echo "Failed to add $dep@$version to $package"
          return 1
        fi
      done
    fi
  fi

  poetry lock
  local lockResult=$?
  if [ "$lockResult" -ne "0" ]; then
    echo "Failed to lock $package"
    return 1
  fi

  poetry install
  local installResult=$?
  if [ "$installResult" -ne "0" ]; then
    echo "Failed to install $package"
    return 1
  fi

  cd $pwd
}

function publishPackage() {
  local package=$1
  local username=$2
  local password=$3

  local pwd=$(echo $PWD)

  cd packages/$package

  isPackagePublished $package $version
  local isPackagePublishedResult=$?
  echo "isPackagePublishedResult: $isPackagePublishedResult"
  if [ "$isPackagePublishedResult" -eq "0" ]; then
    echo "Skip publish: Package $package with version $version is already published"
    return 0
  fi

  poetry publish --build --username $username --password $password
  local publishResult=$?
  if [ "$publishResult" -ne "0" ]; then
    echo "Failed to publish $package"
    return 1
  fi

  cd $pwd
}

# This will only work for the latest version of the package
function isPackagePublished() {
  local package=$1
  local version=$2

  poetry search $package | grep "$package ($version)"
  echo $(poetry search $package | grep "$package ($version)")
  local exit_code=$?
  echo "exit_code: $exit_code"

  if [ "$exit_code" -eq "0" ]; then
    echo "Package $package with version $version is published"
    return 0
  else
    echo "Package $package with version $version is not published"
    return 1
  fi
}

function waitForPackagePublish() {
  local package=$1
  local version=$2
  local seconds=0

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

  if [ "$seconds" -eq "600" ]; then
    echo "Package $package with version $version is not published"
    return 1
  fi
}


# Patching Verion of polywrap-msgpack
echo "Patching Version of polywrap-msgpack to $1"
patchVersion polywrap-msgpack $1
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-msgpack to $1"
  exit 1
fi

echo "Publishing polywrap-msgpack"
publishPackage polywrap-msgpack $2 $3
publishResult=$?
echo "publishResult: $publishResult"
echo  [ "$publishResult" -ne "0" ]
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

# Patching Verion of polywrap-result
echo "Patching Version of polywrap-result to $1"
patchVersion polywrap-result $1
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-result to $1"
  exit 1
fi

echo "Publishing polywrap-result"
publishPackage polywrap-result $2 $3
publishResult=$?
if [ "$publishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-result"
  exit 1
fi

echo "Waiting for the package to be published"
waitForPackagePublish polywrap-result $1
waitForPackagePublishResult=$?
if [ "$waitForPackagePublishResult" -ne "0" ]; then
  echo "Failed to publish polywrap-result"
  exit 1
fi

# Patching Verion of polywrap-manifest
echo "Patching Version of polywrap-manifest to $1"
deps=(polywrap-msgpack polywrap-result)
patchVersion polywrap-manifest $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-manifest to $1"
  exit 1
fi

echo "Publishing polywrap-manifest"
publishPackage polywrap-manifest $2 $3
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

# Patching Verion of polywrap-core
echo "Patching Version of polywrap-core to $1"
deps=(polywrap-result polywrap-manifest)
patchVersion polywrap-core $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-core to $1"
  exit 1
fi

echo "Publishing polywrap-core"
publishPackage polywrap-core $2 $3
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

# Patching Verion of polywrap-wasm
echo "Patching Version of polywrap-wasm to $1"
deps=(polywrap-msgpack polywrap-result polywrap-manifest polywrap-core)
patchVersion polywrap-wasm $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-wasm to $1"
  exit 1
fi

echo "Publishing polywrap-wasm"
publishPackage polywrap-wasm $2 $3
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

# Patching Verion of polywrap-plugin
echo "Patching Version of polywrap-plugin to $1"
deps=(polywrap-msgpack polywrap-result polywrap-manifest polywrap-core)
patchVersion polywrap-plugin $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-plugin to $1"
  exit 1
fi

echo "Publishing polywrap-plugin"
publishPackage polywrap-plugin $2 $3
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

# Patching Verion of polywrap-uri-resolvers
echo "Patching Version of polywrap-uri-resolvers to $1"
deps=(polywrap-result polywrap-wasm polywrap-core)
patchVersion polywrap-uri-resolvers $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-uri-resolvers to $1"
  exit 1
fi

echo "Publishing polywrap-uri-resolvers"
publishPackage polywrap-uri-resolvers $2 $3
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

# Patching Verion of polywrap-client
echo "Patching Version of polywrap-client to $1"
deps=(polywrap-result polywrap-msgpack polywrap-manifest polywrap-core  polywrap-uri-resolvers)
patchVersion polywrap-client $1 deps
patchVersionResult=$?
if [ "$patchVersionResult" -ne "0" ]; then
  echo "Failed to bump version of polywrap-client to $1"
  exit 1
fi

echo "Publishing polywrap-client"
publishPackage polywrap-client $2 $3
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
