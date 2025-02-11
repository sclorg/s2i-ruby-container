import os
import sys

import pytest

from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI
from container_ci_suite.utils import check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")


TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9"
}
TAG = TAGS.get(OS, None)


class TestHelmCakePHPTemplate:

    def setup_method(self):
        package_name = "redhat-ruby-rails-application"
        path = test_dir
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, remote=True)
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_curl_connection(self):
        if self.hc_api.oc_api.shared_cluster:
            pytest.skip("Do NOT test on shared cluster")
        rails_ex_branch = "master"
        if VERSION == "3.3":
            rails_ex_branch = VERSION
        self.hc_api.package_name = "redhat-ruby-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-ruby-rails-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "ruby_version": f"{VERSION}{TAG}",
                "namespace": self.hc_api.namespace,
                "source_repository_ref": rails_ex_branch,
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="rails-example")
        assert self.hc_api.test_helm_curl_output(
            route_name="rails-example",
            expected_str="Welcome to your Rails application"
        )

    def test_by_helm_test(self):
        rails_ex_branch = "master"
        if VERSION == "3.3":
            rails_ex_branch = VERSION
        self.hc_api.package_name = "redhat-ruby-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-ruby-rails-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "ruby_version": f"{VERSION}{TAG}",
                "namespace": self.hc_api.namespace,
                "source_repository_ref": rails_ex_branch,
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="rails-example")
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your Rails application"])
