from inspect import getmembers, iscoroutinefunction
from logging import Logger

from spakky.application.interfaces.container import IPodContainer
from spakky.application.interfaces.post_processor import IPodPostProcessor
from spakky.pod.order import Order
from typer import Typer

from spakky_typer.stereotypes.cli_controller import CliController, TyperCommand
from spakky_typer.utils.asyncio import run_async


@Order(1)
class TyperCLIPostProcessor(IPodPostProcessor):
    __app: Typer
    __logger: Logger

    def __init__(self, app: Typer, logger: Logger) -> None:
        super().__init__()
        self.__app = app
        self.__logger = logger

    def post_process(self, container: IPodContainer, pod: object) -> object:
        if not CliController.exists(pod):
            return pod
        controller = CliController.get(pod)
        command_group: Typer = Typer(name=controller.group_name)
        for _, method in getmembers(pod, callable):
            command: TyperCommand | None = TyperCommand.get_or_none(method)
            if command is not None:
                if iscoroutinefunction(method):
                    method = run_async(method)
                # pylint: disable=line-too-long
                self.__logger.info(
                    f"[{type(self).__name__}] {command.name!r} -> {'async' if iscoroutinefunction(method) else ''} {method.__qualname__}"
                )
                command_group.command(
                    name=command.name,
                    cls=command.cls,
                    context_settings=command.context_settings,
                    help=command.help,
                    epilog=command.epilog,
                    short_help=command.short_help,
                    options_metavar=command.options_metavar,
                    add_help_option=command.add_help_option,
                    no_args_is_help=command.no_args_is_help,
                    hidden=command.hidden,
                    deprecated=command.deprecated,
                    rich_help_panel=command.rich_help_panel,
                )(method)
        self.__app.add_typer(command_group)
        return pod
