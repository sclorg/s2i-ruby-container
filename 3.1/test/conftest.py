import os

import sys

from pathlib import Path
from collections import namedtuple
from pytest import skip

from container_ci_suite.utils import check_variables


if not check_variables():
    sys.exit(1)

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10",
}
BRANCH_TO_TEST = "master"
Vars = namedtuple(
    "Vars",
    [
        "OS",
        "TAG",
        "VERSION",
        "IMAGE_NAME",
        "SHORT_VERSION",
        "TEST_DIR",
        "BRANCH_TO_TEST",
    ],
)
OS = os.getenv("TARGET").lower()
VERSION = os.getenv("VERSION")
BRANCH_TO_TEST = "master"
if VERSION == "3.1" or VERSION == "3.3":
    BRANCH_TO_TEST = "3.3"

VARS = Vars(
    OS=OS,
    TAG=TAGS.get(OS),
    VERSION=VERSION,
    IMAGE_NAME=os.getenv("IMAGE_NAME"),
    SHORT_VERSION=VERSION.replace(".", ""),
    TEST_DIR=Path(__file__).parent.absolute(),
    BRANCH_TO_TEST=BRANCH_TO_TEST,
)


def fips_enabled():
    """
    Check if FIPS is enabled on the system.
    """
    if os.path.exists("/proc/sys/crypto/fips_enabled"):
        return Path("/proc/sys/crypto/fips_enabled").read_text() == "1"
    return False


def skip_fips_tests_rhel8():
    """
    Skip FIPS tests on RHEL8.
    """
    if VARS.OS == "rhel8" and fips_enabled():
        skip("Skipping FIPS tests on RHEL8 because FIPS is enabled.")
