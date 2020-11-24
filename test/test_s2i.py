#!/usr/bin/python3
import logging
import os
import time

from conu import DockerBackend, S2IDockerImage, Probe, DockerRunBuilder

import pytest


image_name = os.environ.get("IMAGE_NAME", "ruby").split(":")[0]
image_tag = os.environ.get("IMAGE_NAME", "ruby").split(":")[1]
test_dir = os.path.abspath(os.path.dirname(__file__))
puma_app_path = os.path.join(test_dir, "puma-test-app")
rack_app_path = os.path.join(test_dir, "rack-test-app")
app_paths = [
    puma_app_path,
    rack_app_path
]


backend = DockerBackend(logging_level=logging.DEBUG)


@pytest.fixture(scope="module", params=app_paths)
def app(request):
    i = S2IDockerImage(image_name, tag=image_tag)
    app_name = os.path.basename(request.param)
    app = i.extend(request.param, app_name)
    yield app
    pass
    app.rmi()


class TestSuite:
    def test_s2i_apps(self, app):
        c = app.run_via_binary()
        try:
            c.wait_for_port(8080)
            assert c.is_port_open(8080)
            response = c.http_request("/", port="8080")
            assert response.ok
            output = c.execute(["bash", "-c", "ruby --version"])[0]
            expected = "ruby %s." % os.environ["VERSION"]
            assert expected in output.decode("utf-8")
        finally:
            c.stop()
            c.wait()
            # debugging
            print(list(c.logs()))
            c.delete()

    def test_invoking_container(self):
        image = backend.ImageClass(image_name, tag=image_tag)
        c = image.run_via_binary(DockerRunBuilder(command=["bash", "-c", "ruby --version"]))
        try:
            c.wait()
            logs = list(c.logs())[0].decode("utf-8")
        finally:
            c.stop()
            c.wait()
            c.delete()
        assert "ruby " in logs
        if os.environ.get("VERSION", None):
            assert os.environ["VERSION"] in logs

    def test_usage(self):
        i = S2IDockerImage(image_name, tag=image_tag)
        c = i.run_via_binary()

        def logs_received():
            return len(list(c.logs())) > 0

        try:
            c.wait()
            # even after waiting there is still a race in journal logging driver
            Probe(timeout=10, pause=0.05, count=20, fnc=logs_received).run()
            logs = [x.decode("utf-8") for x in c.logs()]
            logs = "\n".join(logs).strip()
            usage = i.usage()
            # FIXME: workaround: `docker logs` can't handle logs like these: '\n\n\n'
            assert logs.replace("\n", "") == usage.replace("\n", "")
        finally:
            c.delete()
