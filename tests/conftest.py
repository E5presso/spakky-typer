import logging
from logging import Formatter, StreamHandler, getLogger
from typing import Any, Generator

import pytest
from spakky.application.application import SpakkyApplication
from spakky.application.application_context import ApplicationContext
from spakky.pod.annotations.pod import Pod
from spakky.security.key import Key
from typer import Typer
from typer.testing import CliRunner

from tests import apps


@pytest.fixture(name="key", scope="session")
def get_key_fixture() -> Generator[Key, Any, None]:
    key: Key = Key(size=32)
    yield key


@pytest.fixture(name="cli", scope="function")
def get_cli_fixture(key: Key) -> Generator[Typer, Any, None]:
    logger = getLogger("debug")
    logger.setLevel(logging.DEBUG)
    console = StreamHandler()
    console.setLevel(level=logging.DEBUG)
    console.setFormatter(Formatter("[%(levelname)s][%(asctime)s]: %(message)s"))
    logger.addHandler(console)

    @Pod(name="key")
    def get_key() -> Key:
        return key

    @Pod(name="cli")
    def get_cli() -> Typer:
        return Typer()

    app = (
        SpakkyApplication(ApplicationContext(logger))
        .load_plugins()
        .enable_async_logging()
        .enable_logging()
        .scan(apps)
        .add(get_key)
        .add(get_cli)
    )
    app.start()

    yield app.container.get(type_=Typer)

    app.stop()
    logger.removeHandler(console)


@pytest.fixture(name="runner", scope="function")
def get_runner_fixture() -> Generator[CliRunner, Any, None]:
    runner: CliRunner = CliRunner()
    yield runner
