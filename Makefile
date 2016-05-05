# Variables are documented in hack/build.sh.
BASE_IMAGE_NAME = ruby
VERSIONS = 2.0 2.2 2.3
OPENSHIFT_NAMESPACES = 2.0

# Include common Makefile code.
include hack/common.mk
