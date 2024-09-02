from logging import Logger

from spakky.application.interfaces.pluggable import IPluggable
from spakky.application.interfaces.registry import IPodRegistry
from typer import Typer

from spakky_typer.post_processor import TyperCLIPostProcessor


class TyperCLIPlugin(IPluggable):
    app: Typer
    logger: Logger

    def __init__(self, app: Typer, logger: Logger) -> None:
        self.app = app
        self.logger = logger

    def register(self, registry: IPodRegistry) -> None:
        registry.register_post_processor(
            TyperCLIPostProcessor(
                self.app,
                self.logger,
            )
        )
