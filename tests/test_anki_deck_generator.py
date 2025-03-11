from typer.testing import CliRunner

from anki_deck_generator import __app_name__, __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} version is {__version__}" in result.stdout
