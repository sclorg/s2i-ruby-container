Ruby 2.5 container image
========================
This container image includes Ruby 2.5 as a [S2I](https://github.com/openshift/source-to-image) base image for your Ruby 2.5 applications.
Users can choose between RHEL, CentOS and Fedora based builder images.
The RHEL images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/),
the CentOS images are available on [Quay.io](https://quay.io/organization/centos7),
and the Fedora images are available in [Fedora Registry](https://registry.fedoraproject.org/).
The resulting image can be run using [podman](https://github.com/containers/libpod).

Note: while the examples in this README are calling `podman`, you can replace any such calls by `docker` with the same arguments

Description
-----------

Ruby 2.5 available as container is a base platform for
building and running various Ruby 2.5 applications and frameworks.
Ruby is the interpreted scripting language for quick and easy object-oriented programming.
It has many features to process text files and to do system management tasks (as in Perl).
It is simple, straight-forward, and extensible.

This container image includes an npm utility, so users can use it to install JavaScript
modules for their web applications. There is no guarantee for any specific npm or nodejs
version, that is included in the image; those versions can be changed anytime and
the nodejs itself is included just to make the npm work.

Usage in Openshift
------------------
For this, we will assume that you are using the `ubi8/ruby-25 image`, available via `ruby:2.5` imagestream tag in Openshift.
Building a simple [ruby-sample-app](https://github.com/sclorg/s2i-ruby-container/tree/master/2.5/test/puma-test-app) application
in Openshift can be achieved with the following step:

    ```
    oc new-app ruby:2.5~https://github.com/sclorg/rails-ex.git
    ```

**Accessing the application:**
```
$ oc get pods
$ oc exec <pod> -- curl 127.0.0.1:8080
```

Source-to-Image framework and scripts
-------------------------------------
This image supports the [Source-to-Image](https://docs.openshift.com/container-platform/4.4/builds/build-strategies.html#images-create-s2i_build-strategies)
(S2I) strategy in OpenShift. The Source-to-Image is an OpenShift framework
which makes it easy to write images that take application source code as
an input, use a builder image like this Ruby container image, and produce
a new image that runs the assembled application as an output.

To support the Source-to-Image framework, important scripts are included in the builder image:

* The `/usr/libexec/s2i/assemble` script inside the image is run to produce a new image with the application artifacts. The script takes sources of a given application and places them into appropriate directories inside the image. It utilizes some common patterns in Ruby application development (see the **Environment variables** section below).
* The `/usr/libexec/s2i/run` script is set as the default command in the resulting container image (the new image with the application artifacts). It configures web server and runs this server on port 8080.

Building an application using a Dockerfile
------------------------------------------
Compared to the Source-to-Image strategy, using a Dockerfile is a more
flexible way to build a Ruby container image with an application.
Use a Dockerfile when Source-to-Image is not sufficiently flexible for you or
when you build the image outside of the OpenShift environment.

To use the Ruby image in a Dockerfile, follow these steps:

#### 1. Pull a base builder image to build on

```
podman pull ubi8/ruby-25
```

An RHEL7 image `ubi8/ruby-25` is used in this example.

#### 2. Pull and application code

 An example application available at https://github.com/sclorg/rails-ex.git is used here. Feel free to clone the repository for further experiments.

```
git clone https://github.com/sclorg/rails-ex.git app-src
```

#### 3. Prepare an application inside a container

This step usually consists of at least these parts:

* putting the application source into the container
* installing the dependencies
* setting the default command in the resulting image

For all these three parts, users can use the Source-to-Image scripts inside the image ([3.1.](#31-to-use-the-source-to-image-scripts-and-build-an-image-using-a-dockerfile-create-a-dockerfile-with-this-content)), or users can either setup all manually and use commands `ruby`, `bundle` and `rackup` explicitly in the Dockerfile ([3.2.](32-to-use-your-own-setup-create-a-dockerfile-with-this-content))

##### 3.1 To use the Source-to-Image scripts and build an image using a Dockerfile, create a Dockerfile with this content:
```
FROM ubi8/ruby-25

# Add application sources to a directory that the assemble scriptexpects them
# and set permissions so that the container runs without root access
USER 0
ADD app-src /tmp/src
RUN chown -R 1001:0 /tmp/src
USER 1001

# Set up development mode
ENV RAILS_ENV=development

# Install the dependencies
RUN /usr/libexec/s2i/assemble

# Set the default command for the resulting image
CMD /usr/libexec/s2i/run
```
The s2i scripts are used to set-up and run common Ruby applications. More information about the scripts can be found in [Source-to-Image](#source-to-image-framework-and-scripts) section.
##### 3.2 To use your own setup, create a Dockerfile with this content:
```
FROM ubi8/ruby-25

USER 0
ADD app-src ./
RUN bundle install --path ./bundle

CMD bundle exec "rackup -P /tmp/rack.pid --host 0.0.0.0 --port 8080"
```
#### 4. Build a new image from a Dockerfile prepared in the previous step

```
podman build -t ruby-app .
```

#### 5. Run the resulting image with final application
```
podman run -d ruby-app
```
Environment variables
---------------------

To set these environment variables, you can place them as a key value pair into a `.s2i/environment`
file inside your source code repository.

* **RACK_ENV**

    This variable specifies the environment where the Ruby application will be deployed (unless overwritten) - `production`, `development`, `test`.
    Each level has different behaviors in terms of logging verbosity, error pages, ruby gem installation, etc.

    **Note**: Application assets will be compiled only if the `RACK_ENV` is set to `production`

* **DISABLE_ASSET_COMPILATION**

    This variable set to `true` indicates that the asset compilation process will be skipped. Since this only takes place
    when the application is run in the `production` environment, it should only be used when assets are already compiled.

* **PUMA_MIN_THREADS**, **PUMA_MAX_THREADS**

    These variables indicate the minimum and maximum threads that will be available in [Puma](https://github.com/puma/puma)'s thread pool.

* **PUMA_WORKERS**

    This variable indicate the number of worker processes that will be launched. See documentation on Puma's [clustered mode](https://github.com/puma/puma#clustered-mode).

* **RUBYGEM_MIRROR**

    Set this variable to use a custom RubyGems mirror URL to download required gem packages during build process.

Hot deploy
----------
In order to dynamically pick up changes made in your application source code, you need to make following steps:

*  **For Ruby on Rails applications**

    Run the built Rails image with the `RAILS_ENV=development` environment variable passed to the [podman](https://github.com/containers/libpod) `-e` run flag:
    ```
    $ podman run -e RAILS_ENV=development -p 8080:8080 rails-app
    ```
*  **For other types of Ruby applications (Sinatra, Padrino, etc.)**

    Your application needs to be built with one of gems that reloads the server every time changes in source code are done inside the running container. Those gems are:
    * [Shotgun](https://github.com/rtomayko/shotgun)
    * [Rerun](https://github.com/alexch/rerun)
    * [Rack-livereload](https://github.com/johnbintz/rack-livereload)

    Please note that in order to be able to run your application in development mode, you need to modify the [S2I run script](https://github.com/openshift/source-to-image#anatomy-of-a-builder-image), so the web server is launched by the chosen gem, which checks for changes in the source code.

    After you built your application image with your version of [S2I run script](https://github.com/openshift/source-to-image#anatomy-of-a-builder-image), run the image with the RACK_ENV=development environment variable passed to the [podman](https://github.com/containers/libpod) -e run flag:
    ```
    $ podman run -e RACK_ENV=development -p 8080:8080 sinatra-app
    ```

To change your source code in running container, use Podman's [exec](https://github.com/containers/libpod) command:
```
$ podman exec -it <CONTAINER_ID> /bin/bash
```

After you [podman exec](https://github.com/containers/libpod) into the running container, your current
directory is set to `/opt/app-root/src`, where the source code is located.

Performance tuning
------------------
You can tune the number of threads per worker using the
`PUMA_MIN_THREADS` and `PUMA_MAX_THREADS` environment variables.
Additionally, the number of worker processes is determined by the number of CPU
cores that the container has available, as recommended by
[Puma](https://github.com/puma/puma)'s documentation. This is determined using
the cgroup [cpusets](https://www.kernel.org/doc/Documentation/cgroup-v1/cpusets.txt)
subsystem. You can specify the cores that the container is allowed to use by passing
the `--cpuset-cpus` parameter to the [podman](https://github.com/containers/libpod) run command:
```
$ podman run -e PUMA_MAX_THREADS=32 --cpuset-cpus='0-2,3,5' -p 8080:8080 sinatra-app
```
The number of workers is also limited by the memory limit that is enforced using
cgroups. The builder image assumes that you will need 50 MiB as a base and
another 15 MiB for every worker process plus 128 KiB for each thread. Note that
each worker has its own threads, so the total memory required for the whole
container is computed using the following formula:

```
50 + 15 * WORKERS + 0.125 * WORKERS * PUMA_MAX_THREADS
```
You can specify a memory limit using the `--memory` flag:
```
$ podman run -e PUMA_MAX_THREADS=32 --memory=300m -p 8080:8080 sinatra-app
```
If memory is more limiting then the number of available cores, the number of
workers is scaled down accordingly to fit the above formula. The number of
workers can also be set explicitly by setting `PUMA_WORKERS`.


See also
--------
Dockerfile and other sources are available on https://github.com/sclorg/s2i-ruby-container.
In that repository you also can find another versions of Ruby environment Dockerfiles.
Dockerfile for CentOS is called `Dockerfile`, Dockerfile for RHEL7 is called `Dockerfile.rhel7`,
for RHEL8 it's `Dockerfile.rhel8` and the Fedora Dockerfile is called Dockerfile.fedora.
