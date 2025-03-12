import typer
import time
import os

from rich.console import Console
from rich.panel import Panel
from typing import Optional
from anki_deck_generator import anki_deck_generator, ERRORS, __app_name__, __version__
from pathlib import Path
from typing import Tuple
from typing_extensions import Annotated

app = typer.Typer()
console = Console()

deck_name = "English_Words"
language = "en"
generator = anki_deck_generator.AnkiDeckGenerator("1", deck_name, language)


@app.command()
def dictionary(
    word: Annotated[
        str,
        typer.Option(
            ...,
            "--word",
            "-w",
            help="The word to search for in the dictionary",
            prompt="Enter the word to search for in the dictionary",
        ),
    ],
) -> None:
    measure_time()
    status, data = generator.dictionary(word)

    if status in ERRORS:
        typer.secho(f"{data}", fg=typer.colors.RED)
        raise typer.Exit(1)

    result_text = f"[bold green]Word:[/bold green] {data['word']}\n"
    result_text += f"[bold cyan]Meaning:[/bold cyan] {data['meaning']}\n"
    result_text += f"[bold yellow]Example:[/bold yellow] {data['example']}\n"
    result_text += f"[bold purple]Ipa:[/bold purple] {data['ipa']}"

    console.print(
        Panel(
            result_text, title="📖 Dictionary Result", expand=False, border_style="blue"
        )
    )

    show_time()


@app.command("tts")
def text_to_speech(
    words: Annotated[
        Tuple[str, str],
        typer.Option(
            ...,
            "--words",
            "-w",
            help="The words to convert to speech",
            prompt="Enter the words to convert to speech",
        ),
    ],
) -> None:
    measure_time()
    status, data = generator.text_to_speech(words, True)

    if status in ERRORS:
        typer.secho(f"{data}", fg=typer.colors.RED)
        raise typer.Exit(1)

    result_text = "[bold green]Audios created in this paths:[/bold green]\n\n"

    for i, path in enumerate(data.keys()):
        result_text += (
            f"{Path.home()}/Anki/audios/{path}.mp3{'\n' if i < len(data) - 1 else ''}"
        )

    console.print(
        Panel(result_text, title="🎤 TTS Result", expand=False, border_style="blue")
    )

    show_time()


@app.command("anki")
def generate_anki_deck(
    word: Annotated[
        str,
        typer.Option(
            ...,
            "--word",
            "-w",
            help="The word to create a anki card",
            prompt="Enter the word to create a new anki card",
        ),
    ],
) -> None:
    measure_time()
    status, dict_data = generator.dictionary(word)

    if status in ERRORS:
        typer.secho(f"{dict_data}", fg=typer.colors.RED)
        raise typer.Exit(1)

    dict_text = f"[bold green]Word:[/bold green] {dict_data['word']}\n"
    dict_text += f"[bold cyan]Meaning:[/bold cyan] {dict_data['meaning']}\n"
    dict_text += f"[bold yellow]Example:[/bold yellow] {dict_data['example']}\n"
    dict_text += f"[bold purple]Ipa:[/bold purple] {dict_data['ipa']}"

    console.print(
        Panel(
            dict_text, title="📖 Dictionary Result", expand=False, border_style="blue"
        )
    )

    word = dict_data["word"]
    meaning = dict_data["meaning"]
    example = dict_data["example"]
    ipa = dict_data["ipa"]

    status, tts_data = generator.text_to_speech((word, meaning, example), True)

    if status in ERRORS:
        typer.secho(f"{tts_data}", fg=typer.colors.RED)
        raise typer.Exit(1)

    status, anki_data = generator.create_anki_deck(
        word, ipa, meaning, example, *tts_data.values()
    )

    if status in ERRORS:
        typer.secho(f"{anki_data}", fg=typer.colors.RED)
        raise typer.Exit(1)

    for audio in tts_data.values():
        os.remove(f"{Path.home()}/Anki/audios/{audio}")

    result_text = "[bold green]Anki deck created in this path:[/bold green]\n\n"
    result_text += f"{Path.home()}/Anki/decks/{word}.apkg"

    console.print(
        Panel(result_text, title="🎤 Anki Result", expand=False, border_style="blue")
    )

    show_time()


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
    ),
) -> None:
    return


def measure_time():
    global start_time
    start_time = time.perf_counter()


def show_time():
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if elapsed_time >= 60:
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        formatted_time = f"{minutes}m{seconds}s"
    elif elapsed_time >= 1:
        formatted_time = f"{int(elapsed_time)}s"
    else:
        formatted_time = f"{int(elapsed_time * 1000)}ms"

    console.print(f"[dim]⏱ took {formatted_time}[/dim]")
