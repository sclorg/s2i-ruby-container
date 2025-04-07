import os
import sys

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import check_variables


if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("OS")

SHORT_VERSION = "".join(VERSION.split("."))


class TestRubyImagestreams:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="ruby", version=VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def ruby(self):
        service_name = f"ruby-{SHORT_VERSION}-testing"
        assert self.oc_api.deploy_imagestream_s2i(
            imagestream_file=f"{VERSION}/imagestreams/ruby-rhel.json",
            image_name=IMAGE_NAME,
            app="https://github.com/sclorg/s2i-ruby-container.git",
            context=f"{VERSION}/test/puma-test-app"
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Hello world!"
        )
