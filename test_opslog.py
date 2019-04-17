import os
import pytest
import opslog


def test_get_operator():
    os.environ['OPS_LOG_USER'] = "pytest_operator"
    assert "pytest_operator" == opslog.get_operator()

