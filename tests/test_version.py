import importlib.metadata


def test_package_version(exp_version):
    version = importlib.metadata.version("wtforms-html5")
    assert version == str(exp_version)
