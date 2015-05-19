FROM openshift/base-centos7

# This image provides a Ruby 2.0 environment you can use to run your Ruby
# applications.

MAINTAINER Jakub Hadvig <jhadvig@redhat.com>

EXPOSE 8080

ENV RUBY_VERSION 2.0
LABEL k8s.io/description="Platform for building and running Ruby 2.0 applications" \
      k8s.io/display-name="Ruby 2.0" \
      openshift.io/expose-services="8080:http" \
      openshift.io/tags="builder,ruby,ruby20"

# Copy the STI scripts from the specific language image to /usr/local/sti
COPY ./.sti/bin/ /usr/local/sti

# Each language image can have 'contrib' a directory with extra files needed to
# run and build the applications.
COPY ./contrib/ /opt/openshift

RUN yum install -y \
    https://www.softwarecollections.org/en/scls/rhscl/v8314/epel-7-x86_64/download/rhscl-v8314-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/ruby200/epel-7-x86_64/download/rhscl-ruby200-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/ror40/epel-7-x86_64/download/rhscl-ror40-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/nodejs010/epel-7-x86_64/download/rhscl-nodejs010-epel-7-x86_64.noarch.rpm && \
    yum install -y --setopt=tsflags=nodocs ruby200 ruby200-ruby-devel ruby200-rubygem-rake v8314 ror40-rubygem-bundler ror40-rubygem-rack nodejs010 && \
    yum clean all -y && \
    chown -R default:default /opt/openshift

USER 1001

# Set the default CMD to print the usage of the language image
CMD ["usage"]
