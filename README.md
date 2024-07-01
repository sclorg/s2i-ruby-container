Ruby container images
==================

[![Build and push images to Quay.io registry](https://github.com/sclorg/s2i-ruby-container/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/sclorg/s2i-ruby-container/actions/workflows/build-and-push.yml)

Images available on Quay are:
* Fedora [ruby-30](https://quay.io/repository/fedora/ruby-30)
* Fedora [ruby-31](https://quay.io/repository/fedora/ruby-31)

This repository contains the source for building various versions of
the Ruby application as a reproducible container image using
[source-to-image](https://github.com/openshift/source-to-image).
Users can choose between RHEL and CentOS based builder images.
The resulting image can be run using [podman](https://github.com/containers/libpod).

For more information about using these images with OpenShift, please see the
official [OpenShift Documentation](https://docs.okd.io/latest/using_images/s2i_images/ruby.html).

Versions
---------------
Ruby versions currently provided are:
* [Ruby 2.5](2.5/README.md)
* [Ruby 3.0](3.0/README.md)
* [Ruby 3.1](3.1/README.md)

RHEL versions currently supported are:
* RHEL8
* RHEL9

CentOS versions currently supported are:
* CentOS Stream 9

A Ruby 1.9 image can be built from [this third party repository](https://github.com/getupcloud/s2i-ruby/).
It is not maintained by Red Hat nor is part of the OpenShift project.


Installation
---------------
To build a Ruby image, choose either the CentOS or RHEL based image:
*  **RHEL based image**

    These images are available in the
    [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhel8/ruby-30).
    To download it run:

    ```
    $ podman pull registry.access.redhat.com/rhel8/ruby-30
    ```

    To build a RHEL based Ruby image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-ruby-container.git
    $ cd s2i-ruby-container
    $ make build TARGET=rhel8 VERSIONS=3.0
    ```

*  **CentOS Stream based image**

    This image is available on DockerHub. To download it run:

    ```
    $ podman pull quay.io/sclorg/ruby-30-c9s
    ```

    To build a Ruby image from scratch run:

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-ruby-container.git
    $ cd s2i-ruby-container
    $ make build TARGET=c9s VERSIONS=3.0
    ```

Note: while the installation steps are calling `podman`, you can replace any such calls by `docker` with the same arguments.

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all provided versions of Ruby.**



Usage
---------------------------------

For information about usage of Dockerfile for Ruby 2.5,
see [usage documentation](2.5/README.md).

For information about usage of Dockerfile for Ruby 3.0,
see [usage documentation](3.0/README.md).

For information about usage of Dockerfile for Ruby 3.1,
see [usage documentation](3.1/README.md).

Test
---------------------
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple Ruby application built on top of the s2i-ruby image.

Users can choose between testing a Ruby test application based on a RHEL or CentOS image.

*  **RHEL based image**

    To test a RHEL8-based Ruby image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd s2i-ruby-container
    $ make test TARGET=rhel8 VERSIONS=3.0
    ```

*  **CentOS Stream based image**

    ```
    $ cd s2i-ruby-container
    $ make test TARGET=c9s VERSIONS=3.0
    ```

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all the provided versions of Ruby.**


Repository organization
------------------------
* **`<ruby-version>`**

    Dockerfile and scripts to build container images from.

* **`common/`**

    Folder containing scripts which are responsible for build and test actions performed by the `Makefile`.
    It is a github sub-module pointing to https://github.com/sclorg/container-common-scripts.


Image name structure
------------------------

1. Platform name (lowercase) - ruby
2. Platform version(without dots) - 30
3. Base builder image - c9s/rhel8

Examples: `ruby-30-c9s`, `ruby-30`


Repository organization
------------------------
* **`<ruby-version>`**

    * **Dockerfile.c9s**

        CentOS Stream based Dockerfile.c9s.

    * **Dockerfile.rhel8**

        RHEL based Dockerfile. In order to perform build or test actions on this
        Dockerfile you need to run the action on a properly subscribed RHEL machine.

    * **`s2i/bin/`**

        This folder contains scripts that are run by [S2I](https://github.com/openshift/source-to-image):

        *   **assemble**

            Used to install the sources into the location where the application
            will be run and prepare the application for deployment (eg. installing
            modules using bundler, etc.)

        *   **run**

            This script is responsible for running the application by using the
            application web server.

        *   **usage***

            This script prints the usage of this image.

    * **`root/`**

        This folder contains scripts that are put into the container image.

    * **`test/`**

        This folder contains a [S2I](https://github.com/openshift/source-to-image)
        test framework with a simple Rack server.

        * **`puma-test-app/`**

            Simple Puma web server used for testing purposes by the [S2I](https://github.com/openshift/source-to-image) test framework.

        * **`rack-test-app/`**

            Simple Rack web server used for testing purposes by the [S2I](https://github.com/openshift/source-to-image) test framework.

        * **run**

            Script that runs the [S2I](https://github.com/openshift/source-to-image) test framework.

