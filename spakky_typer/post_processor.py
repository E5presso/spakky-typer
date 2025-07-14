from functools import wraps
from inspect import getmembers, iscoroutinefunction
from logging import Logger
from typing import Any

from spakky.pod.annotations.order import Order
from spakky.pod.annotations.pod import Pod
from spakky.pod.interfaces.aware.container_aware import IContainerAware
from spakky.pod.interfaces.aware.logger_aware import ILoggerAware
from spakky.pod.interfaces.container import IContainer
from spakky.pod.interfaces.post_processor import IPostProcessor
from typer import Typer

from spakky_typer.stereotypes.cli_controller import CliController, TyperCommand
from spakky_typer.utils.asyncio import run_async


@Order(0)
@Pod()
class TyperCLIPostProcessor(IPostProcessor, ILoggerAware, IContainerAware):
    __app: Typer
    __logger: Logger
    __container: IContainer

    def __init__(self, app: Typer) -> None:
        super().__init__()
        self.__app = app

    def set_logger(self, logger: Logger) -> None:
        self.__logger = logger

    def set_container(self, container: IContainer) -> None:
        self.__container = container

    def post_process(self, pod: object) -> object:
        if not CliController.exists(pod):
            return pod
        controller = CliController.get(pod)
        command_group: Typer = Typer(name=controller.group_name)
        for name, method in getmembers(pod, callable):
            command: TyperCommand | None = TyperCommand.get_or_none(method)
            if command is not None:
                # pylint: disable=line-too-long
                self.__logger.info(
                    f"[{type(self).__name__}] {command.name!r} -> {'async' if iscoroutinefunction(method) else ''} {method.__qualname__}"
                )

                @wraps(method)
                def endpoint(
                    *args: Any,
                    method_name: str = name,
                    controller_type: type[object] = controller.type_,
                    container: IContainer = self.__container,
                    **kwargs: Any,
                ) -> Any:
                    controller_instance = container.get(controller_type)
                    method_to_call = getattr(controller_instance, method_name)
                    if iscoroutinefunction(method_to_call):
                        method_to_call = run_async(method_to_call)
                    return method_to_call(*args, **kwargs)

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
                )(endpoint)
        self.__app.add_typer(command_group)
        return pod
