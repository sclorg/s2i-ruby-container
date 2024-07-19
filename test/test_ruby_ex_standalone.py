import os
import sys

import pytest

from container_ci_suite.utils import check_variables
from container_ci_suite.openshift import OpenShiftAPI

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")


# Replacement with 'test_python_s2i_app_ex'
class TestS2IRailsExTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="ruby-testing", version=VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_dancer_ex_template_inside_cluster(self):
        service_name = "ruby-testing"
        rails_ex_branch = "master"
        if VERSION == "3.3":
            rails_ex_branch = VERSION
        assert self.oc_api.deploy_s2i_app(
            image_name=IMAGE_NAME, app=f"https://github.com/sclorg/rails-ex#{rails_ex_branch}",
            context=".",
            service_name=service_name
        )
        assert self.oc_api.template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your Rails application"
        )
