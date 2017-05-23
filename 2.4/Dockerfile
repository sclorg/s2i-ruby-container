FROM centos/s2i-base-centos7

# This image provides a Ruby 2.4 environment you can use to run your Ruby
# applications.

EXPOSE 8080

ENV RUBY_VERSION 2.4

LABEL summary="Platform for building and running Ruby 2.4 applications" \
      io.k8s.description="Platform for building and running Ruby 2.4 applications" \
      io.k8s.display-name="Ruby 2.4" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,ruby,ruby24,rh-ruby24"

# To use subscription inside container yum command has to be run first (before yum-config-manager)
# https://access.redhat.com/solutions/1443553
RUN yum install -y centos-release-scl && \
    yum-config-manager --enable centos-sclo-rh-testing && \
    INSTALL_PKGS="rh-ruby24 rh-ruby24-ruby-devel rh-ruby24-rubygem-rake rh-ruby24-rubygem-bundler rh-nodejs6" && \
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && rpm -V $INSTALL_PKGS && \
    yum clean all -y

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

RUN chown -R 1001:0 /opt/app-root && chmod -R ug+rwx /opt/app-root

USER 1001

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage
