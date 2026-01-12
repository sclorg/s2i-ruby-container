import pytest

from container_ci_suite.helm import HelmChartsAPI

from conftest import VARS


class TestHelmRHELRubyImageStreams:
    def setup_method(self):
        package_name = "redhat-ruby-imagestreams"

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
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("3.3-ubi10", "registry.redhat.io/ubi10/ruby-33:latest", True),
            ("3.3-ubi9", "registry.redhat.io/ubi9/ruby-33:latest", True),
            ("3.3-ubi8", "registry.redhat.io/ubi8/ruby-33:latest", True),
            ("3.0-ubi9", "registry.redhat.io/ubi9/ruby-30:latest", True),
            ("3.0-ubi8", "registry.redhat.io/ubi8/ruby-30:latest", False),
            ("2.5-ubi8", "registry.redhat.io/ubi8/ruby-25:latest", True),
        ],
    )
    def test_package_imagestream(self, version, registry, expected):
        """
        Test checks if Helm imagestreams are present
        """
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert (
            self.hc_api.check_imagestreams(version=version, registry=registry)
            == expected
        )
