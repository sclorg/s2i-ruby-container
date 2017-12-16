Ruby Docker images
==================

[![Build Status](https://travis-ci.org/sclorg/s2i-ruby-container.svg?branch=master)](https://travis-ci.org/sclorg/s2i-ruby-container)


This repository contains the source for building various versions of
the Ruby application as a reproducible Docker image using
[source-to-image](https://github.com/openshift/source-to-image).
Users can choose between RHEL and CentOS based builder images.
The resulting image can be run using [Docker](http://docker.io).

For more information about using these images with OpenShift, please see the
official [OpenShift Documentation](https://docs.openshift.org/latest/using_images/s2i_images/ruby.html).

Versions
---------------
Ruby versions currently provided are:
* [Ruby 2.2](2.2/README.md)
* [Ruby 2.3](2.3/README.md)
* [Ruby 2.4](2.4/README.md)

RHEL versions currently supported are:
* RHEL7

CentOS versions currently supported are:
* CentOS7

A Ruby 1.9 image can be built from [this third party repository](https://github.com/getupcloud/s2i-ruby/).
It is not maintained by Red Hat nor is part of the OpenShift project.


Installation
---------------
To build a Ruby image, choose either the CentOS or RHEL based image:
*  **RHEL based image**

    These images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhscl/ruby-24-rhel7).
    To download it run:

    ```
    $ docker pull registry.access.redhat.com/rhscl/ruby-24-rhel7
    ```

    To build a RHEL based Ruby image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-ruby-container.git
    $ cd s2i-ruby-container
    $ make build TARGET=rhel7 VERSIONS=2.4
    ```

*  **CentOS based image**

    This image is available on DockerHub. To download it run:

    ```
    $ docker pull centos/ruby-24-centos7
    ```

    To build a Ruby image from scratch run:

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-ruby-container.git
    $ cd s2i-ruby-container
    $ make build TARGET=centos7 VERSIONS=2.4
    ```

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all provided versions of Ruby.**



Usage
---------------------------------

For information about usage of Dockerfile for Ruby 2.2,
see [usage documentation](2.2/README.md).

For information about usage of Dockerfile for Ruby 2.3,
see [usage documentation](2.3/README.md).

For information about usage of Dockerfile for Ruby 2.4,
see [usage documentation](2.4/README.md).


Test
---------------------
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple Ruby application built on top of the s2i-ruby image.

Users can choose between testing a Ruby test application based on a RHEL or CentOS image.

*  **RHEL based image**

    To test a RHEL7-based Ruby image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd s2i-ruby-container
    $ make test TARGET=rhel7 VERSIONS=2.4
    ```

*  **CentOS based image**

    ```
    $ cd s2i-ruby-container
    $ make test TARGET=centos7 VERSIONS=2.4
    ```

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all the provided versions of Ruby.**


Repository organization
------------------------
* **`<ruby-version>`**

    Dockerfile and scripts to build container images from.

* **`common/`**

    Folder containing scripts which are responsible for build and test actions performed by the `Makefile`. It is a github sub-module pointing to https://github.com/sclorg/container-common-scripts.


Image name structure
------------------------

1. Platform name (lowercase) - ruby
2. Platform version(without dots) - 24
3. Base builder image - centos7/rhel7

Examples: `ruby-24-centos7`, `ruby-24-rhel7`


Repository organization
------------------------
* **`<ruby-version>`**

    * **Dockerfile**

        CentOS based Dockerfile.

    * **Dockerfile.rhel7**

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

