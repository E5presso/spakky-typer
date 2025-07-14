from click.testing import Result
from spakky.security.key import Key
from typer import Typer
from typer.testing import CliRunner


def test_sync_function(cli: Typer, runner: CliRunner) -> None:
    result: Result = runner.invoke(cli, ["dummy-controller", "sync-function"])
    assert result.exit_code == 0
    assert result.output == "It is synchronous!\n"


def test_first_command(cli: Typer, runner: CliRunner) -> None:
    result: Result = runner.invoke(cli, ["dummy-controller", "first-command"])
    assert result.exit_code == 0
    assert result.output == "First Command!\n"


def test_second_command(cli: Typer, runner: CliRunner) -> None:
    result: Result = runner.invoke(cli, ["dummy-controller", "second-command"])
    assert result.exit_code == 0
    assert result.output == "Second Command!\n"


def test_get_key(cli: Typer, runner: CliRunner, key: Key) -> None:
    result: Result = runner.invoke(cli, ["dummy-controller", "key"])
    assert result.exit_code == 0
    assert result.output == f"Key: {key.hex}\n"


def test_execute_dummy(cli: Typer, runner: CliRunner) -> None:
    result: Result = runner.invoke(cli, ["second", "dummy"])
    assert result.exit_code == 0
    assert result.output == "Just Use Case!\n"
