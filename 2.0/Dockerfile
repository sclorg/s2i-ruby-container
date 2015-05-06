FROM openshift/base-centos7

# This image provides a Ruby 2.0 environment you can use to run your Ruby
# applications.

MAINTAINER Jakub Hadvig <jhadvig@redhat.com>

# Image metadata
ENV RUBY_VERSION=2.0 \
    IMAGE_DESCRIPTION="Ruby 2.0" \
    IMAGE_TAGS=ruby,ruby20 \
    IMAGE_EXPOSE_SERVICES=8080:http

# Copy the STI scripts from the specific language image to /usr/local/sti
COPY ./.sti/bin/ /usr/local/sti

# Each language image can have 'contrib' a directory with extra files needed to
# run and build the applications.
COPY ./contrib/ /opt/openshift

RUN yum install -y \
    https://www.softwarecollections.org/en/scls/rhscl/v8314/epel-7-x86_64/download/rhscl-v8314-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/ruby200/epel-7-x86_64/download/rhscl-ruby200-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/ror40/epel-7-x86_64/download/rhscl-ror40-epel-7-x86_64.noarch.rpm && \
    yum install -y --setopt=tsflags=nodocs ruby200 ruby200-ruby-devel ruby200-rubygem-rake v8314 ror40-rubygem-bundler ror40-rubygem-rack && \
    yum clean all -y && \
    chown -R default:default /opt/openshift

EXPOSE 8080

USER default

# Set the default CMD to print the usage of the language image
CMD ["usage"]
