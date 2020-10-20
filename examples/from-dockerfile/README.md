Dockerfile examples
===================

This directory contains example Dockerfiles that demonstrate how to use the image with a Dockerfile and `docker build`.

For demonstration, we use an application code available at https://github.com/sclorg/rails-ex.git.

Pull the source to the local machine first:
```
git clone https://github.com/sclorg/rails-ex.git app-src
```

Then, build a new image from a Dockerfile in this directory:
```
docker build -f Dockerfile -t ruby-app .
```

And run the resulting image with the final application:
```
docker run -ti --rm ruby-app
```
