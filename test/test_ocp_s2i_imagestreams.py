from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS


class TestRubyImagestreams:
    """
    Test checks if Ruby imagestreams work properly
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

    def ruby_deploy_imagestream(self):
        """
        Test checks if Ruby imagestreams work properly
        """
        service_name = f"ruby-{VARS.SHORT_VERSION}-testing"
        assert self.oc_api.deploy_imagestream_s2i(
            imagestream_file=f"{VARS.VERSION}/imagestreams/ruby-rhel.json",
            image_name=VARS.IMAGE_NAME,
            app="https://github.com/sclorg/s2i-ruby-container.git",
            context=f"{VARS.VERSION}/test/puma-test-app",
            service_name=service_name,
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Hello world!"
        )
