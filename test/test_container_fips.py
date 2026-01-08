import pytest

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper

from conftest import VARS, fips_enabled

fips_test_app = VARS.TEST_DIR / "test-fips"


def build_fips_test_app(app_path: Path) -> ContainerTestLib:
    """
    Build a FIPS test application.
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


class TestRubyFipsModeContainer:
    """
    Test ruby OpenSSL bindings recognize container running in FIPS mode
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

    def test_fips_mode(self):
        """
        Test ruby OpenSSL bindings recognize container running in FIPS mode
        """
        if VARS.OS == "rhel8":
            pytest.skip("Do not execute on RHEL8")
        if fips_enabled():
            # FIPS enabled -> OpenSSL#fips_mode returns true
            output = PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name={VARS.IMAGE_NAME},
                cmd="ruby -ropenssl -e 'exit OpenSSL.fips_mode'",
            )
            assert output
        else:
            # FIPS disabled -> OpenSSL#fips_mode returns false
            output = PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name=f"{VARS.IMAGE_NAME}-{self.app.app_name}",
                cmd="ruby -ropenssl -e 'exit !OpenSSL.fips_mode'",
            )
            assert not output


class TestRubyFipsApplicationContainer:
    """
    Test simple containerized application under FIPS mode
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        self.fips_app = build_fips_test_app(app_path=fips_test_app)

    def teardown_method(self):
        """
        Cleanup the test environment.
        """
        if self.fips_app:
            self.fips_app.cleanup()

    def test_application(self):
        """
        Test crypto algorithms usage for ruby OpenSSL bindings
        with an HTTP app.
        """
        if VARS.OS == "rhel8":
            pytest.skip("Do not execute on RHEL8")
        cid_file_name = self.fips_app.app_name
        assert self.fips_app.create_container(
            cid_file_name=cid_file_name, container_args="--user 100001"
        )
        cid = self.fips_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.fips_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # The endpoints respond with HTTP 200 as a success
        # The endpoints respond with HTTP status 500 for FIPS related failures,
        # where a cipher behaved incorrectly.
        # In the case of unexpected errors, app responds with HTTP status 409
        # If HTTP status code is 409 or 500, the response body also contains
        # a message including a backtrace.
        assert self.fips_app.test_response(
            url=f"http://{cip}",
            page="/symmetric/aes-256-cbc",
            debug=True,
        )
        assert self.fips_app.test_response(
            url=f"http://{cip}",
            page="/symmetric/des-ede-cbc",
            debug=True,
        )
        assert self.fips_app.test_response(
            url=f"http://{cip}",
            page="/hash/sha256",
            debug=True,
        )
        assert self.fips_app.test_response(
            url=f"http://{cip}",
            page="/hash/md5",
            debug=True,
        )
