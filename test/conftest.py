import os

import sys

from pathlib import Path
from collections import namedtuple

from container_ci_suite.utils import check_variables

PSQL_TAGS = {
    "rhel8": "-el8",
    "rhel9": "-el9",
    "rhel10": "-el10",
}
if not check_variables():
    sys.exit(1)

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10",
}
TEST_DIR = Path(__file__).parent.absolute()
APPS = [
    TEST_DIR / f"{x}test-app"
    for x in [
        "",
        "puma-",
        "rack-",
    ]
]
Vars = namedtuple(
    "Vars",
    [
        "OS",
        "TAG",
        "VERSION",
        "IMAGE_NAME",
        "SHORT_VERSION",
        "TEST_DIR",
        "APPS",
        "TEST_APP_BRANCH",
        "PSQL_TAG",
        "PSQL_IMAGE_SHORT",
        "PSQL_IMAGE_TAG",
        "DEPLOYED_PSQL_IMAGE",
    ],
)
OS = os.getenv("TARGET").lower()
VERSION = os.getenv("VERSION")
PSQL_TAG = PSQL_TAGS.get(OS)
PSQL_IMAGE_SHORT = f"postgresql:12{PSQL_TAG}"
PSQL_IMAGE_TAG = f"12{PSQL_TAG}"
TEST_APP_BRANCH = "master"
if VERSION and float(VERSION) >= 3.1:
    TEST_APP_BRANCH = "3.3"
DEPLOYED_PSQL_IMAGE = "quay.io/sclorg/postgresql-12-c8s"
VARS = Vars(
    OS=OS,
    TAG=TAGS.get(OS),
    VERSION=VERSION,
    IMAGE_NAME=os.getenv("IMAGE_NAME"),
    SHORT_VERSION=VERSION.replace(".", ""),
    TEST_DIR=TEST_DIR,
    APPS=APPS,
    TEST_APP_BRANCH=TEST_APP_BRANCH,
    PSQL_TAG=PSQL_TAGS.get(OS),
    PSQL_IMAGE_SHORT=PSQL_IMAGE_SHORT,
    PSQL_IMAGE_TAG=PSQL_IMAGE_TAG,
    DEPLOYED_PSQL_IMAGE=DEPLOYED_PSQL_IMAGE,
)


def fips_enabled():
    """
    Check if FIPS is enabled on the system.
    """
    if os.path.exists("/proc/sys/crypto/fips_enabled"):
        return Path("/proc/sys/crypto/fips_enabled").read_text() == "1"
    return False
