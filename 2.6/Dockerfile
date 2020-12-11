FROM quay.io/centos7/s2i-base-centos7

# This image provides a Ruby environment you can use to run your Ruby
# applications.

EXPOSE 8080

ENV RUBY_MAJOR_VERSION=2 \
    RUBY_MINOR_VERSION=6

ENV RUBY_VERSION="${RUBY_MAJOR_VERSION}.${RUBY_MINOR_VERSION}" \
    RUBY_SCL_NAME_VERSION="${RUBY_MAJOR_VERSION}${RUBY_MINOR_VERSION}"

# Set SCL related variables in Dockerfile so that the collection is enabled by default
ENV RUBY_SCL="rh-ruby${RUBY_SCL_NAME_VERSION}" \
    IMAGE_NAME="centos7/ruby-${RUBY_SCL_NAME_VERSION}-centos7" \
    SUMMARY="Platform for building and running Ruby $RUBY_VERSION applications" \
    DESCRIPTION="Ruby $RUBY_VERSION available as container is a base platform for \
building and running various Ruby $RUBY_VERSION applications and frameworks. \
Ruby is the interpreted scripting language for quick and easy object-oriented programming. \
It has many features to process text files and to do system management tasks (as in Perl). \
It is simple, straight-forward, and extensible." \
    PATH=$PATH:/opt/rh/$NODEJS_SCL/root/usr/bin:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/local/bin:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/bin:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/bin:/opt/rh/$NODEJS_SCL/root/usr/bin \
    LD_LIBRARY_PATH=/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/lib64:/opt/rh/$NODEJS_SCL/root/usr/lib64:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/local/lib64 \
    X_SCLS=$X_SCLS:rh-ruby$RUBY_SCL_NAME_VERSION \
    MANPATH=/opt/rh/$NODEJS_SCL/root/usr/share/man:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/local/share/man:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/share/man:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/local/man:/share/man/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/share/man:/opt/rh/$NODEJS_SCL/root/usr/share/man \
    PYTHONPATH=/opt/rh/$NODEJS_SCL/root/usr/lib/python2.7/site-packages \
    XDG_DATA_DIRS=/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/local/share:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/share \
    PKG_CONFIG_PATH=/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/local/lib64/pkgconfig:/opt/rh/rh-ruby$RUBY_SCL_NAME_VERSION/root/usr/lib64/pkgconfig
LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Ruby ${RUBY_VERSION}" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,ruby,ruby${RUBY_SCL_NAME_VERSION},${RUBY_SCL}" \
      com.redhat.component="${RUBY_SCL}-container" \
      name="${IMAGE_NAME}" \
      version="${RUBY_VERSION}" \
      usage="s2i build https://github.com/sclorg/s2i-ruby-container.git \
--context-dir=${RUBY_VERSION}/test/puma-test-app/ ${IMAGE_NAME} ruby-sample-app" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>"

RUN yum install -y centos-release-scl-rh && \
    INSTALL_PKGS=" \
libffi-devel \
${RUBY_SCL} \
${RUBY_SCL}-ruby-devel \
${RUBY_SCL}-rubygem-rake \
${RUBY_SCL}-rubygem-bundler \
" && \
    yum install -y --setopt=tsflags=nodocs ${INSTALL_PKGS} && \
    yum -y clean all --enablerepo='*' && \
    rpm -V ${INSTALL_PKGS}

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# Drop the root user and make the content of /opt/app-root owned by user 1001
RUN chown -R 1001:0 ${APP_ROOT} && chmod -R ug+rwx ${APP_ROOT} && \
    rpm-file-permissions

USER 1001

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage
