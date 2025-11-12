from container_ci_suite.helm import HelmChartsAPI

from conftest import VARS


class TestHelmCakePHPTemplate:
    """
    Test checks if Helm imagestream and Helm ruby rails application
    works properly and response is as expected.
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        package_name = "redhat-ruby-rails-application"
        self.hc_api = HelmChartsAPI(
            path=VARS.TEST_DIR,
            package_name=package_name,
            tarball_dir=VARS.TEST_DIR,
            shared_cluster=True,
        )
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts",
            repo_name="helm-charts",
            subdir="charts/redhat",
        )

    def teardown_method(self):
        """
        Teardown the test environment.
        """
        self.hc_api.delete_project()

    def test_by_helm_test(self):
        """
        Test checks if Helm imagestream and Helm ruby rails application
        works properly and response is as expected.
        """
        self.hc_api.package_name = "redhat-ruby-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-ruby-rails-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "ruby_version": f"{VARS.VERSION}{VARS.TAG}",
                "namespace": self.hc_api.namespace,
                "source_repository_ref": VARS.BRANCH_TO_TEST,
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="rails-example")
        assert self.hc_api.test_helm_chart(
            expected_str=["Welcome to your Rails application"]
        )
