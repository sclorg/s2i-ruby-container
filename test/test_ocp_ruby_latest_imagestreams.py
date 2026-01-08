from container_ci_suite.imagestreams import ImageStreamChecker

from conftest import VARS


class TestLatestImagestreams:
    """
    Test if local imagestreams are the latest one
    """

    def setup_method(self):
        """
        Setup the test environment.
        """
        self.isc = ImageStreamChecker(working_dir=VARS.TEST_DIR.parent.parent)

    def test_latest_imagestream(self):
        """
        Test if local imagestreams are the latest one
        """
        self.latest_version = self.isc.get_latest_version()
        assert self.latest_version
        self.isc.check_imagestreams(self.latest_version)
