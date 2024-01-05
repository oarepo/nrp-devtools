import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_repository_dir():
    """Create a temporary directory for testing."""
    test_dir = "temporary_test_repository"
    if os.path.exists(test_dir) and not os.environ.get("NRP_TEST_KEEP_TEMPORARY_DIR"):
        shutil.rmtree(test_dir)
    yield test_dir


@pytest.fixture(scope="session")
def absolute_test_repository_dir(test_repository_dir):
    yield Path(test_repository_dir).resolve()