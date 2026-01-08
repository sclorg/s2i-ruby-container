import pytest

from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS


class TestS2IRailsTemplates:
    """
    Test if Ruby s2i local templates work properly
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        self.oc_api = OpenShiftAPI(
            pod_name_prefix=f"ruby-{VARS.SHORT_VERSION}-testing",
            version=VARS.VERSION,
            shared_cluster=True,
        )

    def teardown_method(self):
        """
        Teardown the test environment.
        """
        self.oc_api.delete_project()

    @pytest.mark.parametrize(
        "template_type",
        [
            "local",
            "ex",
        ],
    )
    def test_rails_template_inside_cluster(self, template_type):
        """
        Test if Ruby s2i local templates work properly
        """
        assert self.oc_api.upload_image(
            VARS.DEPLOYED_PGSQL_IMAGE, VARS.PSQL_IMAGE_SHORT
        )
        service_name = f"ruby-{VARS.SHORT_VERSION}-testing"
        if template_type == "local":
            template_url = "examples/rails.json"
        else:
            template_url = self.oc_api.get_raw_url_for_json(
                container="rails-ex",
                dir="openshift/templates",
                filename="rails.json",
                branch=VARS.TEST_APP_BRANCH,
            )
        openshift_args = [
            "SOURCE_REPOSITORY_URL=https://github.com/sclorg/rails-ex.git",
            f"SOURCE_REPOSITORY_REF={VARS.TEST_APP_BRANCH}",
            f"RUBY_VERSION={VARS.VERSION}",
            f"NAME={service_name}",
        ]
        # TODO: Add postgresql persistent template
        # if template != "rails.json":
        #     openshift_args = [
        #         "SOURCE_REPOSITORY_URL=https://github.com/sclorg/rails-ex.git",
        #         f"SOURCE_REPOSITORY_REF={VARS.TEST_APP_BRANCH}",
        #         f"POSTGRESQL_VERSION={VARS.PSQL_IMAGE_TAG}",
        #         f"RUBY_VERSION={VARS.VERSION}",
        #         f"NAME={service_name}",
        #         "DATABASE_USER=testu",
        #         "DATABASE_PASSWORD=testp",
        #     ]
        assert self.oc_api.deploy_template_with_image(
            image_name=VARS.IMAGE_NAME,
            template=template_url,
            name_in_template="ruby",
            openshift_args=openshift_args,
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name,
            expected_output="Welcome to your Rails application",
        )
