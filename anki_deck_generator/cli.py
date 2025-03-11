import typer

from rich.console import Console
from rich.panel import Panel
from typing import Optional
from anki_deck_generator import anki_deck_generator, ERRORS, __app_name__, __version__


app = typer.Typer()
generator = anki_deck_generator.AnkiDeckGenerator("123", "English_Words", "en")
console = Console()


@app.command()
def dictionary(
    word: str = typer.Option(
        None,
        "--word",
        "-w",
        help="The word to search for in the dictionary",
        prompt="Enter the word to search for in the dictionary",
    )
) -> None:
    status, data = generator.dictionary(word)

    if status in ERRORS:
        typer.secho(f"{data}", fg=typer.colors.RED)
        raise typer.Exit(1)

    result_text = f"[bold green]Word:[/bold green] {data['word']}\n"
    result_text += f"[bold cyan]Meaning:[/bold cyan] {data['meaning']}\n"
    result_text += f"[bold yellow]Example:[/bold yellow] {data['example']}"

    console.print(
        Panel(
            result_text, title="📖 Dictionary Result", expand=False, border_style="blue"
        )
    )


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} version is {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version of the app and exit",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
