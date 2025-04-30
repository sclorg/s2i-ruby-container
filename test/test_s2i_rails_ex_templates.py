import os
import sys

import pytest

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")

DEPLOYED_PGSQL_IMAGE = "quay.io/sclorg/postgresql-12-c8s"

TAGS = {
    "rhel8": "-el8",
    "rhel9": "-el9"
}
TAG = TAGS.get(OS, None)
IMAGE_SHORT = f"postgresql:12{TAG}"
IMAGE_TAG = f"12{TAG}"

SHORT_VERSION = "".join(VERSION.split("."))


class TestS2IRailsExTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix=f"ruby-{SHORT_VERSION}-testing", version=VERSION, shared_cluster=True)
        assert self.oc_api.upload_image(DEPLOYED_PGSQL_IMAGE, IMAGE_SHORT)

    def teardown_method(self):
        self.oc_api.delete_project()

    @pytest.mark.parametrize(
        "template",
        [
            "rails.json",
            "rails-postgresql-persistent.json"
        ]
    )
    def test_rails_template_inside_cluster(self, template):
        if OS == "rhel10":
            pytest.skip("Do NOT test on rhel10")
        service_name = f"ruby-{SHORT_VERSION}-testing"
        rails_ex_branch = "master"
        if VERSION == "3.3":
            rails_ex_branch = VERSION
        template_url = self.oc_api.get_raw_url_for_json(
            container="rails-ex", dir="openshift/templates", filename=template, branch=rails_ex_branch
        )
        openshift_args = [
            f"SOURCE_REPOSITORY_URL=https://github.com/sclorg/rails-ex.git",
            f"SOURCE_REPOSITORY_REF={rails_ex_branch}",
            f"RUBY_VERSION={VERSION}",
            f"NAME={service_name}"
        ]
        if template != "rails.json":
            openshift_args = [
                f"SOURCE_REPOSITORY_URL=https://github.com/sclorg/rails-ex.git",
                f"SOURCE_REPOSITORY_REF={rails_ex_branch}",
                f"POSTGRESQL_VERSION={IMAGE_TAG}",
                f"RUBY_VERSION={VERSION}",
                f"NAME={service_name}",
                f"DATABASE_USER=testu",
                f"DATABASE_PASSWORD=testp"
            ]
        assert self.oc_api.deploy_template_with_image(
            image_name=IMAGE_NAME,
            template=template_url,
            name_in_template="ruby",
            openshift_args=openshift_args
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your Rails application"
        )
