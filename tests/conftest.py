import pytest
from packaging.version import Version

from wtforms_html5 import MINMAX_VALIDATORS
from wtforms_html5 import MINMAXLENGTH_VALIDATORS

EXP_VERSION = "0.6.1"


@pytest.fixture(scope="session")
def exp_version() -> Version:
    version = Version(EXP_VERSION)
    return version


@pytest.fixture(scope="session", params=MINMAX_VALIDATORS)
def minmax_validator(request):
    return request.param


@pytest.fixture(scope="session", params=MINMAXLENGTH_VALIDATORS)
def minmaxlength_validator(request):
    return request.param
