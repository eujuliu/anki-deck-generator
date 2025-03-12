import os
from typer.testing import CliRunner
from anki_deck_generator import __app_name__, __version__, cli
from pathlib import Path

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} version is {__version__}" in result.stdout


def test_dictionary():
    result = runner.invoke(cli.app, ["dictionary", "--word", "hello"])

    assert result.exit_code == 0
    assert "Word" in result.stdout
    assert "Meaning" in result.stdout
    assert "Example" in result.stdout
    assert "Ipa" in result.stdout


def test_text_to_speech():
    result = runner.invoke(cli.app, ["tts", "--words", "hello", "world"])

    hello_mp3_path = Path(f"{Path.home()}/Anki/audios/hello.mp3")
    world_mp3_path = Path(f"{Path.home()}/Anki/audios/world.mp3")

    assert result.exit_code == 0
    assert hello_mp3_path.is_file()
    assert world_mp3_path.is_file()

    os.remove(hello_mp3_path)
    os.remove(world_mp3_path)
