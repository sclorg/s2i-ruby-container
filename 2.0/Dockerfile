FROM openshift/base-centos7

ENV STI_RUBY_VERSION 2.0

RUN yum install -y \
    https://www.softwarecollections.org/en/scls/rhscl/v8314/epel-7-x86_64/download/rhscl-v8314-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/ruby200/epel-7-x86_64/download/rhscl-ruby200-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/ror40/epel-7-x86_64/download/rhscl-ror40-epel-7-x86_64.noarch.rpm && \
    yum install -y --setopt=tsflags=nodocs ruby200 ruby200-ruby-devel ruby200-rubygem-rake v8314 ror40-rubygem-bundler && \
    yum clean all -y

USER default

# Copy the ruby scripts and build tools into /opt/openshift directory
# TODO: There is a bug in Docker < 1.5 that disallows to use './..' as destination directory.
COPY ./ruby /opt/openshift/

EXPOSE 9292
