import os

from pathlib import Path
from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.utils import ContainerTestLibUtils
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper

from conftest import VARS


test_app = VARS.TEST_DIR / "test-app"
puma_test_app = VARS.TEST_DIR / "puma-test-app"
rack_test_app = VARS.TEST_DIR / "rack-test-app"

test_ports = PodmanCLIWrapper.podman_inspect(
    field="{{range $key, $value := .Config.ExposedPorts }}{{$key}}{{end}}",
    src_image=VARS.IMAGE_NAME,
).split("/")
print(f"The exposed ports are: {test_ports}")


def build_s2i_app(app_path: Path) -> ContainerTestLib:
    """
    Build a S2I application.
    """
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    app_name = app_path.name
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args="--pull-policy=never",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-{app_name}",
    )
    return s2i_app


class TestRubyHelloWorldContainer:
    """
    Test if container works under specific user
    and not only with user --user 10001
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        if "test-app" not in os.listdir(VARS.TEST_DIR):
            ContainerTestLibUtils.run_command(
                "git clone https://github.com/openshift/ruby-hello-world.git test-app"
            )
        self.s2i_app = build_s2i_app(app_path=test_app)

    def teardown_method(self):
        """
        Cleanup the test environment.
        """
        self.s2i_app.cleanup()

    def test_application(self):
        """
        Test if container works under specific user
        and not only with user --user 100001
        """
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name, container_args="--user 100001"
        )
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # ruby --version returns proper version
        assert (
            f"ruby {VARS.VERSION}."
            in PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name=f"{VARS.IMAGE_NAME}-{cid_file_name}", cmd="ruby --version"
            )
        )
        # Response code from HTTP url is 200
        assert self.s2i_app.test_response(url=f"http://{cip}", port=test_ports[0])


class TestRubyPumaTestAppContainer:
    """
    Test if container works under specific user
    and not only with user --user 10001
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        self.s2i_app = build_s2i_app(app_path=puma_test_app)

    def teardown_method(self):
        """
        Cleanup the test environment.
        """
        self.s2i_app.cleanup()

    def test_application(self):
        """
        Test if container works under specific user
        and not only with user --user 10001
        """
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name, container_args="--user 100001"
        )
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # ruby --version returns proper version
        assert (
            f"ruby {VARS.VERSION}."
            in PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name=f"{VARS.IMAGE_NAME}-{cid_file_name}", cmd="ruby --version"
            )
        )
        # Response code from HTTP url is 200
        assert self.s2i_app.test_response(url=f"http://{cip}", port=test_ports[0])


class TestRubyRackTestAppContainer:
    """
    Test if container works under specific user
    and not only with user --user 10001
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        self.s2i_app = build_s2i_app(app_path=rack_test_app)

    def teardown_method(self):
        """
        Cleanup the test environment.
        """
        self.s2i_app.cleanup()

    def test_application(self):
        """
        Test if container works under specific user
        and not only with user --user 10001
        """
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name, container_args="--user 100001"
        )
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # ruby --version returns proper version
        assert (
            f"ruby {VARS.VERSION}."
            in PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name=f"{VARS.IMAGE_NAME}-{cid_file_name}", cmd="ruby --version"
            )
        )
        # Response code from HTTP url is 200
        assert self.s2i_app.test_response(url=f"http://{cip}", port=test_ports[0])
