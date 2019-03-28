Ruby 2.4 container image
=================

This container image includes Ruby 2.4 as a [S2I](https://github.com/openshift/source-to-image) base image for your Ruby 2.4 applications.
Users can choose between RHEL, CentOS and Fedora based builder images.
The RHEL images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/),
the CentOS images are available on [Docker Hub](https://hub.docker.com/r/centos/),
and the Fedora images are available in [Fedora Registry](https://registry.fedoraproject.org/).
The resulting image can be run using [podman](https://github.com/containers/libpod).

Note: while the examples in this README are calling `podman`, you can replace any such calls by `docker` with the same arguments

Description
-----------

Ruby 2.4 available as container is a base platform for 
building and running various Ruby 2.4 applications and frameworks. 
Ruby is the interpreted scripting language for quick and easy object-oriented programming. 
It has many features to process text files and to do system management tasks (as in Perl). 
It is simple, straight-forward, and extensible.

This container image includes an npm utility, so users can use it to install JavaScript
modules for their web applications. There is no guarantee for any specific npm or nodejs
version, that is included in the image; those versions can be changed anytime and
the nodejs itself is included just to make the npm work.

Usage
---------------------
For this, we will assume that you are using the `rhscl/ruby-24-rhel7 image`, available via `ruby:2.4` imagestream tag in Openshift.
Building a simple [ruby-sample-app](https://github.com/sclorg/s2i-ruby-container/tree/master/2.4/test/puma-test-app) application
in Openshift can be achieved with the following step:

    ```
    oc new-app ruby:2.4~https://github.com/sclorg/s2i-ruby-container.git --context-dir=2.4/test/puma-test-app/
    ```

The same application can also be built using the standalone [S2I](https://github.com/openshift/source-to-image) application on systems that have it available:

    ```
    $ s2i build https://github.com/sclorg/s2i-ruby-container.git --context-dir=2.4/test/puma-test-app/ rhscl/ruby-24-rhel7 ruby-sample-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```

Environment variables
---------------------

To set these environment variables, you can place them as a key value pair into a `.sti/environment`
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
---------------------
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
podman exec -it <CONTAINER_ID> /bin/bash
```

After you [podman exec](https://github.com/containers/libpod) into the running container, your current
directory is set to `/opt/app-root/src`, where the source code is located.

Performance tuning
---------------------
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
In that repository you also can find another versions of Python environment Dockerfiles.
Dockerfile for CentOS is called `Dockerfile`, Dockerfile for RHEL7 is called `Dockerfile.rhel7`,
for RHEL8 it's `Dockerfile.rhel8` and the Fedora Dockerfile is called Dockerfile.fedora.
