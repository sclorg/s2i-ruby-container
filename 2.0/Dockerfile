FROM openshift/base-centos7

# This image provides a Ruby 2.0 environment you can use to run your Ruby
# applications.

MAINTAINER Jakub Hadvig <jhadvig@redhat.com>

# Image metadata
ENV RUBY_VERSION          = "2.0" \
    IMAGE_DESCRIPTION     = "Ruby 2.0" \
    IMAGE_TAGS            = "ruby,ruby20" \
    IMAGE_EXPOSE_SERVICES = "8080:http"

RUN yum install -y \
    https://www.softwarecollections.org/en/scls/rhscl/v8314/epel-7-x86_64/download/rhscl-v8314-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/ruby200/epel-7-x86_64/download/rhscl-ruby200-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/ror40/epel-7-x86_64/download/rhscl-ror40-epel-7-x86_64.noarch.rpm && \
    yum install -y --setopt=tsflags=nodocs ruby200 ruby200-ruby-devel ruby200-rubygem-rake v8314 ror40-rubygem-bundler && \
    yum clean all -y

USER default

EXPOSE 8080
