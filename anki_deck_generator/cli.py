import typer
import time

from rich.console import Console
from rich.panel import Panel
from typing import Optional

from anki_deck_generator import ERRORS, __app_name__, __version__
from anki_deck_generator.generator import Generator
from anki_deck_generator.database import Database
from pathlib import Path
from typing import Tuple
from typing_extensions import Annotated

app = typer.Typer()
console = Console()


def init():
    global generator
    global database
    generator = Generator("English Words", "en")
    database = Database(f"{typer.get_app_dir(__app_name__)}/database.json")


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
    meaning: Optional[str] = typer.Option(
        None,
        "--meaning",
        "-m",
        help="The meaning of the word",
    ),
    example: Optional[str] = typer.Option(
        None,
        "--example",
        "-e",
        help="The example of the word",
    ),
    ipa: Optional[str] = typer.Option(
        None,
        "--ipa",
        "-i",
        help="The ipa of the word",
    ),
    override: Optional[bool] = typer.Option(
        None,
        "--override",
        "-o",
        help="Override the word if it already exists",
    ),
) -> None:
    measure_time()

    word = word.lower().strip()
    data = database.read(word)

    exists = data is not None and data.get("status", None) == "created"

    if exists and data.get("result", None):
        meaning = data["result"]["meaning"]
        example = data["result"]["example"]
        ipa = data["result"]["ipa"]

    if not all([meaning, example, ipa]):
        status, dict_data = generator.dictionary(word)

        if status in ERRORS:
            typer.secho(f"{dict_data}", fg=typer.colors.RED)
            database.write(word, {"status": "error", "error": str(dict_data)})
            raise typer.Exit(1)

        if not meaning:
            meaning = dict_data["meaning"]
        if not example:
            example = dict_data["example"]
        if not ipa:
            ipa = dict_data["ipa"]

        data = database.write(
            word,
            {
                **(data if data else {}),
                "result": {"meaning": meaning, "example": example, "ipa": ipa},
            },
        )

    dict_text = f"[bold green]Word:[/bold green] {word}\n"
    dict_text += f"[bold cyan]Meaning:[/bold cyan] {meaning}\n"
    dict_text += f"[bold yellow]Example:[/bold yellow] {example}\n"
    dict_text += f"[bold purple]Ipa:[/bold purple] {ipa}"

    console.print(
        Panel(
            dict_text,
            title="📖 Dictionary Result",
            expand=False,
            border_style="blue",
        )
    )

    if exists and not override:
        typer.secho(
            "ERROR: This word is already added (use --override for override)",
            fg=typer.colors.RED,
        )
        show_time()
        raise typer.Exit(1)

    data = database.write(word, {**data, "status": "creating"})

    status, tts_data = generator.text_to_speech((word, meaning, example), create=True)

    if status in ERRORS:
        typer.secho(f"{tts_data}", fg=typer.colors.RED)
        database.write(word, {"status": "error", "error": str(tts_data)})
        remove_audio_files()
        raise typer.Exit(1)

    status, anki_data = generator.create_anki_deck(
        word, ipa, meaning, example, *tts_data.values()
    )

    if status in ERRORS:
        typer.secho(f"{anki_data}", fg=typer.colors.RED)
        database.write(word, {"status": "error", "error": str(anki_data)})
        remove_audio_files()
        raise typer.Exit(1)

    result_text = "[bold green]Anki deck created in this path:[/bold green]\n\n"
    result_text += anki_data["path"]

    console.print(
        Panel(result_text, title="🎤 Anki Result", expand=False, border_style="blue")
    )

    database.write(
        word,
        {
            "status": "created",
            "result": {
                "meaning": meaning,
                "example": example,
                "ipa": ipa,
            },
        },
    )
    remove_audio_files()
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
):
    init()

    return


def remove_audio_files():
    audios_path = Path(f"{Path.home()}/Anki/audios")
    for audio in audios_path.iterdir():
        audio.unlink()


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
