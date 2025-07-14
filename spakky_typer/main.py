from spakky.application.application import SpakkyApplication

from spakky_typer.post_processor import TyperCLIPostProcessor


def initialize(app: SpakkyApplication) -> None:
    app.add(TyperCLIPostProcessor)
