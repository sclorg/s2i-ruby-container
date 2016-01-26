FROM openshift/base-centos7

# This image provides a Ruby 1.9 environment you can use to run your Ruby
# applications.

MAINTAINER SoftwareCollections.org <sclorg@redhat.com>

EXPOSE 8080

ENV RUBY_VERSION 1.9

LABEL io.k8s.description="Platform for building and running Ruby 1.9 applications" \
      io.k8s.display-name="Ruby 1.9" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,ruby,ruby19"

RUN INSTALL_PKGS="ruby193 ruby193-ruby ruby193-ruby-devel ruby193-rubygem-rake v8314 ruby193-rubygem-rails nodejs010" && \
    yum install -y centos-release-scl && \
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && rpm -V $INSTALL_PKGS && \
    yum clean all -y

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Each language image can have 'contrib' a directory with extra files needed to
# run and build the applications.
COPY ./contrib/ /opt/app-root

RUN chown -R 1001:0 /opt/app-root

USER 1001

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage
