from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS


class TestS2IRailsExTemplate:
    """
    Test checks if Ruby ex standalone template works properly and response is as expected.
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        self.oc_api = OpenShiftAPI(
            pod_name_prefix=f"ruby-{VARS.SHORT_VERSION}-testing", version=VARS.VERSION
        )

    def teardown_method(self):
        """
        Teardown the test environment.
        """
        self.oc_api.delete_project()

    def test_dancer_ex_template_inside_cluster(self):
        """
        Test checks if Ruby ex standalone template works properly and response is as expected.
        """
        service_name = f"ruby-{VARS.SHORT_VERSION}-testing"
        assert self.oc_api.deploy_s2i_app(
            image_name=VARS.IMAGE_NAME,
            app=f"https://github.com/sclorg/rails-ex#{VARS.BRANCH_TO_TEST}",
            context=".",
            service_name=service_name,
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name,
            expected_output="Welcome to your Rails application",
        )
