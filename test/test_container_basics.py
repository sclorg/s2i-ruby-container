import os

import pytest

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.utils import ContainerTestLibUtils

from conftest import VARS


def build_npm_app(app_path: Path) -> ContainerTestLib:
    """
    Build a S2I application.
    """
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args="--pull-policy=never",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-testapp",
    )
    return s2i_app


class TestS2IRubyContainer:
    """
    Test if container works properly
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        self.app = ContainerTestLib()

    def teardown_method(self):
        """
        Cleanup the test environment.
        """
        self.app.cleanup()

    def test_run_s2i_usage(self):
        """
        Test if s2i usage works
        """
        assert self.app.s2i_usage()

    def test_docker_run_usage(self):
        """
        Test if container is runnable
        """
        assert (
            PodmanCLIWrapper.call_podman_command(
                cmd=f"run --rm {VARS.IMAGE_NAME} &>/dev/null", return_output=False
            )
            == 0
        )

    def test_scl_usage(self):
        """
        Test if ruby --version returns proper output
        """
        assert (
            f"ruby {VARS.VERSION}."
            in PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name=VARS.IMAGE_NAME, cmd="ruby --version"
            )
        )

    @pytest.mark.parametrize("dockerfile", ["Dockerfile", "Dockerfile.s2i"])
    def test_dockerfiles(self, dockerfile):
        Test if building apps based on Containerfiles in
        examples/ works
        assert self.app.build_test_container(
            dockerfile=VARS.TEST_DIR / "examples/from-dockerfile" / dockerfile,
            app_url=f"https://github.com/sclorg/rails-ex.git@{VARS.BRANCH_TO_TEST}",
            app_dir="app-src",
        )
        assert self.app.test_app_dockerfile()
        cip = self.app.get_cip()
        assert cip
        assert self.app.test_response(
            url=cip, expected_output="Welcome to your Rails application on OpenShift"
        )


class TestRubyNPMtestContainer:
    """
    Test NPM is valid and works properly
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        if "test-app" not in os.listdir(VARS.TEST_DIR):
            ContainerTestLibUtils.run_command(
                "git clone https://github.com/openshift/ruby-hello-world.git test-app"
            )
        self.s2i_app = build_npm_app(VARS.TEST_DIR / "test-app")

    def teardown_method(self):
        """
        Cleanup the test environment.
        """
        self.s2i_app.cleanup()

    def test_npm_works(self):
        """
        Test checks if NPM is valid and works properly
        """
        assert self.s2i_app.npm_works(image_name=VARS.IMAGE_NAME)
