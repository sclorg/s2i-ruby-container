import os
import pytest

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.utils import ContainerTestLibUtils
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper

from conftest import VARS


test_ports = PodmanCLIWrapper.podman_inspect(
    field="{{range $key, $value := .Config.ExposedPorts }}{{$key}}{{end}}",
    src_image=VARS.IMAGE_NAME,
)
print(f"The exposed ports are: {test_ports}")

if "test-app" not in os.listdir(VARS.TEST_DIR):
    ContainerTestLibUtils.run_command(
        "git clone https://github.com/openshift/ruby-hello-world.git test-app"
    )


class TestRubyApplicationContainer:
    @pytest.fixture(
        scope="class", params=VARS.APPS, ids=[app.name for app in VARS.APPS]
    )
    def build_s2i_app(self, request):
        container_lib = ContainerTestLib(VARS.IMAGE_NAME)
        app_name = request.param.name
        s2i_app = container_lib.build_as_df(
            app_path=request.param,
            s2i_args="--pull-policy=never",
            src_image=VARS.IMAGE_NAME,
            dst_image=f"{VARS.IMAGE_NAME}-{app_name}",
        )
        yield s2i_app
        s2i_app.cleanup()

    def test_application(self, build_s2i_app):
        """
        Test if container works under specific user
        and not only with user --user 100001
        """
        cid_file_name = build_s2i_app.app_name
        assert build_s2i_app.create_container(
            cid_file_name=cid_file_name, container_args="--user 100001"
        )
        cip = build_s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # ruby --version returns proper version
        assert (
            f"ruby {VARS.VERSION}."
            in PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name=f"{VARS.IMAGE_NAME}-{cid_file_name}", cmd="ruby --version"
            )
        )
        # Response code from HTTP url is 200
        assert build_s2i_app.test_response(
            url=f"http://{cip}", port=test_ports.split("/")[0]
        )
