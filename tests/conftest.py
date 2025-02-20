"""Sahred pytest configuration and fixtures"""
import os
import re
from pathlib import Path

import pytest
from panel.config import panel_extension
from panel.io.state import state

# pylint: disable=protected-access
EXAMPLES_PATH = Path(__file__).parent.parent / "examples"

# The fixtures in this module are heavily inspired the Panel conftest.py file.


def get_default_port():
    """to get a different starting port per worker for pytest-xdist"""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "0")
    factor = int(re.sub(r"\D", "", worker_id))
    return 6000 + factor * 30


PORT = [get_default_port()]


@pytest.fixture
def port() -> int:
    """Returns an available port"""
    PORT[0] += 1
    return PORT[0]


@pytest.fixture(autouse=True)
def module_cleanup():
    """
    Cleanup Panel extensions after each test.
    """
    from bokeh.core.has_props import (
        _default_resolver,
    )  # pylint: disable=import-outside-toplevel

    to_reset = list(panel_extension._imports.values())

    _default_resolver._known_models = {
        name: model
        for name, model in _default_resolver._known_models.items()
        if not any(model.__module__.startswith(tr) for tr in to_reset)
    }


@pytest.fixture(autouse=True)
def server_cleanup():
    """
    Clean up server state after each test.
    """
    try:
        yield
    finally:
        state.reset()


@pytest.fixture(autouse=True)
def cache_cleanup():
    """Clean up the state caches"""
    state.clear_caches()


def _get_paths():
    paths = []
    for folder in sorted(EXAMPLES_PATH.glob("**/"), key=lambda folder: folder.name):
        if folder.name == "examples":
            continue

        for file in folder.glob("*.py"):
            paths.append(str(file))

    return paths


APP_PATHS = _get_paths()


@pytest.fixture(params=APP_PATHS)
def app_path(request) -> str:
    """Returns a path to an app .py file"""
    return request.param
