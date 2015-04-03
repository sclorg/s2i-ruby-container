Ruby for OpenShift - Docker images
========================================

This repository contains sources of the images for building various versions
of Ruby applications as reproducible Docker images using
[source-to-image](https://github.com/openshift/source-to-image).
User can choose between RHEL and CentOS based builder images.
The resulting image can be run using [Docker](http://docker.io).


Versions
---------------
Ruby versions currently provided are:
* ruby-2.0

RHEL versions currently supported are:
* RHEL7

CentOS versions currently supported are:
* CentOS7


Installation
---------------
To build Ruby image, choose between CentOS or RHEL based image:
*  **RHEL based image**

    To build a rhel-based ruby-2.0 image, you need to run the build on properly
    subscribed RHEL machine.

    ```
    $ git clone https://github.com/openshift/sti-ruby.git
    $ cd sti-ruby
    $ make build TARGET=rhel7 VERSION=2.0
    ```

*  **CentOS based image**

    This image is available on DockerHub. To download it use:

    ```
    $ docker pull openshift/ruby-20-centos7
    ```

    To build Ruby image from scratch use:

    ```
    $ git clone https://github.com/openshift/sti-ruby.git
    $ cd sti-ruby
    $ make build VERSION=2.0
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all provided versions of Ruby. Since we are now providing only version `2.0`,
you can omit this parameter.**


Usage
---------------------
To build a simple [ruby-sample-app](https://github.com/openshift/sti-ruby/tree/master/2.0/test/puma-test-app) application,
using standalone [STI](https://github.com/openshift/source-to-image) and then run the
resulting image with [Docker](http://docker.io) execute:

*  **For RHEL based image**
    ```
    $ sti build https://github.com/openshift/sti-ruby.git --contextDir=2.0/test/puma-test-app/ openshift/ruby-20-rhel7 ruby-sample-app
    $ docker run -p 8080:8080 ruby-sample-app
    ```

*  **For CentOS based image**
    ```
    $ sti build https://github.com/openshift/sti-ruby.git --contextDir=2.0/test/puma-test-app/ openshift/ruby-20-centos7 ruby-sample-app
    $ docker run -p 8080:8080 ruby-sample-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```


Test
---------------------
This repository also provides [STI](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple ruby application built on top of sti-ruby image.

User can choose between testing ruby test application based on RHEL or CentOS image.

*  **RHEL based image**

    To test a rhel7-based ruby-2.0 image, you need to run the test on properly
    subscribed RHEL machine.

    ```
    $ cd sti-ruby
    $ make test TARGET=rhel7 VERSION=2.0
    ```

*  **CentOS based image**

    ```
    $ cd sti-ruby
    $ make test VERSION=2.0
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all the provided versions of Ruby. Since we are now providing only version `2.0`
you can omit this parameter.**


Repository organization
------------------------
* **`<ruby-version>`**

    * **Dockerfile**

        CentOS based Dockerfile.

    * **Dockerfile.rhel7**

        RHEL based Dockerfile. In order to perform build or test actions on this
        Dockerfile you need to run the action on properly subscribed RHEL machine.

    * **`.sti/bin/`**

        This folder contains scripts that are run by [STI](https://github.com/openshift/source-to-image):

        *   **assemble**

            Is used to install the sources into location from where the application
            will be run and prepare the application for deployment (eg. installing
            modules using bundler, etc.)

        *   **run**

            This script is responsible for running the application, by using the
            application web server.

        *   **usage***

            This script prints the usage of this image.

    * **`contrib/`**

        This folder contains file with commonly used modules.

    * **`test/`**

        This folder is containing [STI](https://github.com/openshift/source-to-image)
        test framework with simple Rack server.

        * **`puma-test-app/`**

            Simple Puma web server used for testing purposes in the [STI](https://github.com/openshift/source-to-image) test framework.

        * **`rack-test-app/`**

            Simple Rack web server used for testing purposes in the [STI](https://github.com/openshift/source-to-image) test framework.

        * **run**

            Script that runs the [STI](https://github.com/openshift/source-to-image) test framework.

* **`hack/`**

    Folder contains scripts which are responsible for build and test actions performed by the `Makefile`.


Image name structure
------------------------
##### Structure: openshift/1-2-3

1. Platform name - ruby
2. Platform version(without dots)
3. Base builder image - centos7/rhel7

Examples: `openshift/ruby-20-centos7`, `openshift/ruby-20-rhel7`


Environment variables
---------------------

To set these environment variables, you can place them into `.sti/environment`
file inside your source code repository.

* **RACK_ENV**

    This variable specifies in what environment should the ruby application be deployed - `production`, `development`, `test`.
    Each level has different behavior in terms of logging verbosity, error pages, ruby gem installation, etc.

    **Note**: The application assets are going to be compiled only if the `RACK_ENV` is set to `production`

* **RAILS_ENV**

    This variable specifies in what environment should the ruby application be deployed - `production`, `development`, `test`.
    Each level has different behavior in terms of logging verbosity, error pages, ruby gem installation, etc.

    **Note**: The application assets are going to be compiled only if the `RAILS_ENV` is set to `production`

* **DISABLE_ASSET_COMPILATION**

    This variable indicates that the process of asset compilation will be skipped. Since the process of asset compilation
    takes place only when the application runs in `production` environment, it should be used when assets are already compiled.
