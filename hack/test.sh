#!/bin/bash -e
# $1 - Specifies distribution - RHEL7/CentOS7
# $2 - Specifies Ruby version - 2.0

# Array of all versions of Ruby
declare -a VERSIONS=(2.0)

OS=$1
VERSION=$2

if [ -z ${VERSION} ]; then
  # Build all versions
  dirs=${VERSIONS}
else
  # Build only specified version on Ruby
  dirs=${VERSION}
fi

for dir in ${dirs}; do
  IMAGE_NAME=openshift/ruby-${dir//./}-${OS}
  echo ">>>> Testing ${IMAGE_NAME}"

  pushd ${dir} > /dev/null

  if [ "$OS" == "rhel7" ]; then
    mv Dockerfile Dockerfile.centos7
    mv Dockerfile.rhel7 Dockerfile
    trap "mv Dockerfile Dockerfile.rhel7 && mv Dockerfile.centos7 Dockerfile" RETURN
    docker build -t ${IMAGE_NAME}-candidate .
    IMAGE_NAME=${IMAGE_NAME}-candidate test/run
  else
    docker build -t ${IMAGE_NAME}-candidate .
    IMAGE_NAME=${IMAGE_NAME}-candidate test/run
  fi

  popd > /dev/null
done
