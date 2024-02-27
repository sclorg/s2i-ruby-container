#!/bin/bash
#
# Functions for tests for the Ruby S2I image in OpenShift.
#
# IMAGE_NAME specifies a name of the candidate image used for testing.
# The image has to be available before this script is executed.
#

THISDIR=$(dirname ${BASH_SOURCE[0]})

source "${THISDIR}/test-lib.sh"
source "${THISDIR}/test-lib-openshift.sh"

function ct_pull_or_import_postgresql() {
  postgresql_image="quay.io/sclorg/postgresql-12-c8s"
  image_short="postgresql:12"
  image_tag="${image_short}"
  # Variable CVP is set by CVP pipeline
  if [ "${CVP:-0}" -eq "0" ]; then
    # In case of container or OpenShift 4 tests
    # Pull image before going through tests
    # Exit in case of failure, because postgresql container is mandatory
    ct_pull_image "${postgresql_image}" "true"
  else
    # Import postgresql-10-centos7 image before running tests on CVP
    oc import-image "${image_short}:latest" --from="${postgresql_image}:latest" --insecure=true --confirm
    # Tag postgresql image to "postgresql:10" which is expected by test suite
    oc tag "${image_short}:latest" "${image_tag}"
  fi
}

function rails_ex_branch() {
  # Ruby 3.3 introduced too many incompatibilities to be able
  # to use the same Gemfile for RHEL 7 and also newer RHELs.
  # we can use the same Gemfile for RHEL 7 and newer
  # as long as Ruby MAJOR.MINOR <= 3.1. Newer Ruby needs dependencies
  # that are not compatible with RHEL 7.

  # Latest stable
  rails_example_repo_branch="3.3"
  if { echo "$VERSION"; echo "3.1"; } | sort --version-sort --check=quiet; then
    # Ruby 3.1 and prior.
    rails_example_repo_branch="master"
  fi

  echo "$rails_example_repo_branch"
}

function test_ruby_integration() {
  ct_os_test_s2i_app "${IMAGE_NAME}" \
                     "https://github.com/sclorg/s2i-ruby-container.git" \
                     "${VERSION}/test/puma-test-app" \
                     ".*"
}

# Check the imagestream
function test_ruby_imagestream() {

  ct_os_test_image_stream_s2i "${THISDIR}/imagestreams/ruby-${OS%[0-9]*}.json" "${IMAGE_NAME}" \
                              "https://github.com/sclorg/s2i-ruby-container.git" \
                              "${VERSION}/test/puma-test-app" \
                              ".*"
}

function test_ruby_s2i_rails_app() {
  ct_os_test_s2i_app "${IMAGE_NAME}" \
                    "https://github.com/sclorg/rails-ex#master" \
                    . \
                    'Welcome to your Rails application'
}


function test_ruby_s2i_rails_templates() {
  # TODO: this was not working because the referenced example dir was added as part of this commit
  ct_os_test_template_app "${IMAGE_NAME}" \
                        "https://raw.githubusercontent.com/sclorg/rails-ex/master/openshift/templates/rails.json" \
                        "ruby" \
                        "Welcome to your Rails application" \
                        8080 http 200 \
                        "-p SOURCE_REPOSITORY_REF=$(rails_ex_branch) -p SOURCE_REPOSITORY_URL=https://github.com/sclorg/rails-ex -p RUBY_VERSION=${VERSION} -p NAME=ruby-testing" \
                        "quay.io/sclorg/postgresql-12-c8s|postgresql:12-el8"
}

function test_ruby_s2i_rails_persistent_templates() {
  # TODO: this was not working because the referenced example dir was added as part of this commit
  if [ "${OS}" == "rhel7" ]; then
    echo "Skip testing Rails Template with Persistent storage on RHEL7."
    return 0
  fi
  ct_os_test_template_app "${IMAGE_NAME}" \
                        "https://raw.githubusercontent.com/sclorg/rails-ex/master/openshift/templates/rails-postgresql-persistent.json" \
                        "ruby" \
                        "Welcome to your Rails application" \
                        8080 http 200 \
                        "-p SOURCE_REPOSITORY_REF=$(rails_ex_branch) -p SOURCE_REPOSITORY_URL=https://github.com/sclorg/rails-ex -p RUBY_VERSION=${VERSION} -p POSTGRESQL_VERSION=12-el8 -p NAME=ruby-testing \
                         -p DATABASE_USER=testu \
                         -p DATABASE_PASSWORD=testp" \
                        "quay.io/sclorg/postgresql-12-c8s|postgresql:12-el8"
}


function test_ruby_s2i_local_persistent_templates() {
  # TODO: this was not working because the referenced example dir was added as part of this commit
  if [ "${OS}" == "rhel7" ]; then
    echo "Skip testing Rails Template with Persistent storage on RHEL7."
    return 0
  fi
  ct_os_test_template_app "${IMAGE_NAME}" \
                        "${THISDIR}/examples/rails-postgresql-persistent.json" \
                        "ruby" \
                        "Welcome to your Rails application" \
                        8080 http 200 \
                        "-p SOURCE_REPOSITORY_REF=$(rails_ex_branch) -p SOURCE_REPOSITORY_URL=https://github.com/sclorg/rails-ex -p RUBY_VERSION=${VERSION} -p POSTGRESQL_VERSION=12-el8 -p NAME=ruby-testing \
                         -p DATABASE_USER=testu \
                         -p DATABASE_PASSWORD=testp" \
                        "quay.io/sclorg/postgresql-12-c8s|postgresql:12-el8"
}

function test_ruby_s2i_local_app_templates() {
  # TODO: this was not working because the referenced example dir was added as part of this commit
  ct_os_test_template_app "${IMAGE_NAME}" \
                        "${THISDIR}/examples/rails.json" \
                        "ruby" \
                        "Welcome to your Rails application" \
                        8080 http 200 \
                        "-p SOURCE_REPOSITORY_REF=$(rails_ex_branch) -p SOURCE_REPOSITORY_URL=https://github.com/sclorg/rails-ex -p RUBY_VERSION=${VERSION} -p NAME=ruby-testing" \
                        "quay.io/sclorg/postgresql-12-c8s|postgresql:12-el8"
}

function test_latest_imagestreams() {
  local result=1
  # Switch to root directory of a container
  pushd "${THISDIR}/../.." >/dev/null || return 1
  ct_check_latest_imagestreams
  result=$?
  popd >/dev/null || return 1
  return $result
}

# vim: set tabstop=2:shiftwidth=2:expandtab:

