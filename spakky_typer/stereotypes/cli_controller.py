from dataclasses import dataclass
from typing import Any, Callable

from spakky.core.annotation import FunctionAnnotation
from spakky.core.types import AnyT, FuncT
from spakky.pod.annotations.pod import Pod
from typer.core import TyperCommand as TyperCommandClass
from typer.models import Default

from spakky_typer.utils.casing import pascal_to_kebab


@dataclass
class TyperCommand(FunctionAnnotation):
    name: str | None = None
    cls: type[TyperCommandClass] | None = None
    context_settings: dict[Any, Any] | None = None
    help: str | None = None
    epilog: str | None = None
    short_help: str | None = None
    options_metavar: str = "[OPTIONS]"
    add_help_option: bool = True
    no_args_is_help: bool = False
    hidden: bool = False
    deprecated: bool = False
    rich_help_panel: str | None = Default(None)


def command(
    name: str | None = None,
    cls: type[TyperCommandClass] | None = None,
    context_settings: dict[Any, Any] | None = None,
    help: str | None = None,
    epilog: str | None = None,
    short_help: str | None = None,
    options_metavar: str = "[OPTIONS]",
    add_help_option: bool = True,
    no_args_is_help: bool = False,
    hidden: bool = False,
    deprecated: bool = False,
    rich_help_panel: str | None = Default(None),
) -> Callable[[FuncT], FuncT]:
    def wrapper(method: FuncT) -> FuncT:
        return TyperCommand(
            name=name,
            cls=cls,
            context_settings=context_settings,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
            rich_help_panel=rich_help_panel,
        )(method)

    return wrapper


@dataclass(eq=False)
class CliController(Pod):
    group_name: str | None = None

    def __call__(self, obj: AnyT) -> AnyT:
        if self.group_name is None:
            self.group_name = pascal_to_kebab(obj.__name__)
        return super().__call__(obj)
