from logging import Logger

from spakky.application.application_context import ApplicationContext
from spakky.application.interfaces.pluggable import IPluggable
from typer import Typer

from spakky_typer.plugins.typer_cli import TyperCLIPlugin
from spakky_typer.post_processor import TyperCLIPostProcessor


def test_fast_api_plugin_register(logger: Logger) -> None:
    app: Typer = Typer()
    context: ApplicationContext = ApplicationContext()
    plugin: IPluggable = TyperCLIPlugin(app, logger)
    plugin.register(context)

    assert context.post_processors == {TyperCLIPostProcessor}
