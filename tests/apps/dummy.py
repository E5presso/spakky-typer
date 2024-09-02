from spakky.security.key import Key
from spakky.stereotype.usecase import UseCase

from spakky_typer.stereotypes.api_controller import CliController, command


@UseCase()
class DummyUseCase:
    async def execute(self) -> str:
        return "Just Use Case!"


@CliController()
class DummyController:
    __key: Key

    def __init__(self, key: Key) -> None:
        self.__key = key

    async def just_function(self) -> str:
        return "Just Function!"

    @command()
    def sync_function(self) -> None:
        print("It is synchronous!")

    @command()
    async def first_command(self) -> None:
        print("First Command!")

    @command()
    async def second_command(self) -> None:
        print("Second Command!")

    @command("key")
    async def get_key(self) -> None:
        print(f"Key: {self.__key.hex}")


@CliController("second")
class SecondDummyController:
    __usecase: DummyUseCase

    def __init__(self, usecase: DummyUseCase) -> None:
        self.__usecase = usecase

    @command("dummy")
    async def execute_dummy(self) -> None:
        print(await self.__usecase.execute())
