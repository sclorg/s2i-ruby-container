#!/bin/bash -e
# $1 - Specifies distribution - RHEL7/CentOS7
OS=$1
VERSION=$2

# Array of all versions of Ruby
declare -a VERSIONS=(2.0)

# TODO: Remove this hack once Docker 1.5 is in use, 
# which supports building of named Dockerfiles.
function docker_build {
  TAG=$1
  DOCKERFILE=$2

  if [ -n "$DOCKERFILE" -a "$DOCKERFILE" != "Dockerfile" ]; then
    # Swap Dockerfiles and setup a trap restoring them
    mv Dockerfile Dockerfile.centos7
    mv "${DOCKERFILE}" Dockerfile
    trap "mv Dockerfile ${DOCKERFILE} && mv Dockerfile.centos7 Dockerfile" ERR RETURN
  fi

  docker build -t ${TAG} . && trap - ERR
}

if [ -z ${VERSION} ]; then
  # Build all versions
  dirs=${VERSIONS}
else
  # Build only specified version on Ruby
  dirs=${VERSION}
fi

for dir in ${dirs[@]}; do
  IMAGE_NAME=openshift/ruby-${dir//./}-${OS}
  echo ">>>> Building ${IMAGE_NAME}"

  pushd ${dir} > /dev/null

  if [ "$OS" == "rhel7" -o "$OS" == "rhel7-candidate" ]; then
    docker_build ${IMAGE_NAME} Dockerfile.rhel7
  else
    docker_build ${IMAGE_NAME}
  fi

  popd > /dev/null
done
