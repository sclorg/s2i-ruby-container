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

#function test_ruby_s2i_rails_app() {
#  ct_os_test_s2i_app "${IMAGE_NAME}" \
#                    "https://github.com/phracek/rails-ex#bump_template_to_30" \
#                    . \
#                    'Welcome to your Dancer application on OpenShift'
#}


function test_ruby_s2i_templates() {
  # TODO: this was not working because the referenced example dir was added as part of this commit
  ct_os_test_template_app "${IMAGE_NAME}" \
                        "${THISDIR}/rails-postgresql.json" \
                        ruby \
                        "Everything is OK" \
                        8080 http 200 \
                        "-p SOURCE_REPOSITORY_REF=master -p VERSION=${VERSION} -p NAME=rails-postgresql-example"
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

