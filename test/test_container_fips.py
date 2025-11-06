from pathlib import Path
from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper

from conftest import VARS, skip_fips_tests_rhel8, fips_enabled

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
    Test if container works under specific user
    and not only with user --user 10001
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
        Test if container works under specific user
        and not only with user --user 10001
        """
        print(f"Is FIPS enabled? {fips_enabled()}")
        if fips_enabled():
            output = PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name={VARS.IMAGE_NAME},
                cmd="ruby -ropenssl -e 'exit OpenSSL.fips_mode'",
            )
            print(f"FIPS is enabled {output}")
            assert output
        else:
            output = PodmanCLIWrapper.podman_run_command_and_remove(
                cid_file_name=f"{VARS.IMAGE_NAME}-{self.app.app_name}",
                cmd="ruby -ropenssl -e 'exit !OpenSSL.fips_mode'",
            )
            print(f"FIPS is disable {output}")
            assert not output


class TestRubyFipsApplicationContainer:
    """
    Test if container works under specific user
    and not only with user --user 100001
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
        self.fips_app.cleanup()

    def test_application(self):
        """
        Test if container works under specific user
        and not only with user --user 100001
        """
        skip_fips_tests_rhel8()
        cid_file_name = self.fips_app.app_name
        assert self.fips_app.create_container(
            cid_file_name=cid_file_name, container_args="--user 100001"
        )
        cid = self.fips_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.fips_app.get_cip(cid_file_name=cid_file_name)
        assert cip
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
