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


@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/redhat", package_name="ruby-imagestreams", tarball_dir=test_dir)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()


class TestHelmRHELRubyImageStreams:

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("3.3-ubi9", "registry.redhat.io/ubi9/ruby-33:latest", True),
            ("3.3-ubi8", "registry.redhat.io/ubi8/ruby-33:latest", True),
            ("3.1-ubi9", "registry.redhat.io/ubi9/ruby-31:latest", True),
            ("3.1-ubi8", "registry.redhat.io/ubi8/ruby-31:latest", True),
            ("3.0-ubi9", "registry.redhat.io/ubi9/ruby-30:latest", True),
            ("3.0-ubi8", "registry.redhat.io/ubi8/ruby-30:latest", False),
            ("2.5-ubi8", "registry.redhat.io/ubi8/ruby-25:latest", True),
        ],
    )
    def test_package_imagestream(self, helm_api, version, registry, expected):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry) == expected
