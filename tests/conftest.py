import logging
from typing import Any, Generator
from logging import Logger, Formatter, StreamHandler, getLogger

import pytest
from spakky.application.application_context import ApplicationContext
from spakky.plugins.aspect import AspectPlugin
from spakky.plugins.logging import LoggingPlugin
from spakky.pod.pod import Pod
from spakky.security.key import Key
from typer import Typer
from typer.testing import CliRunner

from spakky_typer.plugins.typer_cli import TyperCLIPlugin
from tests import apps


@pytest.fixture(name="key", scope="session")
def get_key_fixture() -> Generator[Key, Any, None]:
    key: Key = Key(size=32)
    yield key


@pytest.fixture(name="logger", scope="session")
def get_logger_fixture() -> Generator[Logger, Any, None]:
    logger: Logger = getLogger("debug")
    logger.setLevel(logging.DEBUG)
    console = StreamHandler()
    console.setLevel(level=logging.DEBUG)
    console.setFormatter(Formatter("[%(levelname)s] (%(asctime)s) : %(message)s"))
    logger.addHandler(console)

    yield logger

    logger.removeHandler(console)


@pytest.fixture(name="app", scope="function")
def get_app_fixture(key: Key, logger: Logger) -> Generator[Typer, Any, None]:
    @Pod(name="logger")
    def get_logger() -> Logger:
        return logger

    @Pod(name="key")
    def get_key() -> Key:
        return key

    app: Typer = Typer()
    context: ApplicationContext = ApplicationContext(package=apps)

    context.register_plugin(LoggingPlugin())
    context.register_plugin(TyperCLIPlugin(app, logger))
    context.register_plugin(AspectPlugin(logger))

    context.register(get_logger)
    context.register(get_key)

    context.start()
    yield app


@pytest.fixture(name="runner", scope="function")
def get_runner_fixture() -> Generator[CliRunner, Any, None]:
    runner: CliRunner = CliRunner()
    yield runner
