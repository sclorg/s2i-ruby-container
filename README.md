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
* ruby-2.0
* ruby-2.2
* ruby-2.3

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

    To build a RHEL based Ruby image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone https://github.com/sclorg/s2i-ruby-container.git
    $ cd s2i-ruby
    $ make build TARGET=rhel7 VERSION=2.0
    ```

*  **CentOS based image**

    This image is available on DockerHub. To download it run:

    ```
    $ docker pull openshift/ruby-20-centos7
    ```

    To build a Ruby image from scratch run:

    ```
    $ git clone https://github.com/sclorg/s2i-ruby-container.git
    $ cd s2i-ruby
    $ make build VERSION=2.0
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all provided versions of Ruby.**



Usage
---------------------------------

For information about usage of Dockerfile for Ruby 2.0,
see [usage documentation](2.0/README.md).

For information about usage of Dockerfile for Ruby 2.2,
see [usage documentation](2.2/README.md).

For information about usage of Dockerfile for Ruby 2.3,
see [usage documentation](2.3/README.md).


Test
---------------------
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple Ruby application built on top of the s2i-ruby image.

Users can choose between testing a Ruby test application based on a RHEL or CentOS image.

*  **RHEL based image**

    To test a RHEL7-based Ruby-2.0 image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd s2i-ruby
    $ make test TARGET=rhel7 VERSION=2.0
    ```

*  **CentOS based image**

    ```
    $ cd s2i-ruby
    $ make test VERSION=2.0
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all the provided versions of Ruby.**


Repository organization
------------------------
* **`<ruby-version>`**

    Dockerfile and scripts to build container images from.

* **`hack/`**

    Folder containing scripts which are responsible for build and test actions performed by the `Makefile`.


Image name structure
------------------------
##### Structure: openshift/1-2-3

1. Platform name (lowercase) - ruby
2. Platform version(without dots) - 20
3. Base builder image - centos7/rhel7

Examples: `openshift/ruby-20-centos7`, `openshift/ruby-20-rhel7`
