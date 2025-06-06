import os
import sys

from container_ci_suite.utils import check_variables
from container_ci_suite.openshift import OpenShiftAPI

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")

SHORT_VERSION = "".join(VERSION.split("."))

# Replacement with 'test_python_s2i_app_ex'
class TestS2IRubyTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix=f"ruby-{SHORT_VERSION}-testing", version=VERSION, shared_cluster=True)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_rails_template_inside_cluster(self):
        service_name = f"ruby-{SHORT_VERSION}-testing"
        assert self.oc_api.deploy_s2i_app(
            image_name=IMAGE_NAME, app=f"https://github.com/sclorg/s2i-ruby-container.git",
            context=f"{VERSION}/test/puma-test-app",
            service_name=service_name
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Hello world!"
        )
