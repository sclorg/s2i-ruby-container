# Variables are documented in hack/build.sh.
BASE_IMAGE_NAME = ruby
VERSIONS = 1.9 2.0 2.2
OPENSHIFT_NAMESPACES = 2.0

# Include common Makefile code.
include hack/common.mk
