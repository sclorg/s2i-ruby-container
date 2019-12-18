# Variables are documented in common/build.sh.
BASE_IMAGE_NAME = ruby
VERSIONS = 2.4 2.5 2.6
OPENSHIFT_NAMESPACES = 2.0
CONU_IMAGE := docker.io/usercont/conu:0.6.2

# HACK:  Ensure that 'git pull' for old clones doesn't cause confusion.
# New clones should use '--recursive'.
.PHONY: $(shell test -f common/common.mk || echo >&2 'Please do "git submodule update --init" first.')

include common/common.mk
