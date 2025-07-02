import typer

from vecna.commands import app as commands_app

app = typer.Typer()

app.add_typer(commands_app)


if __name__ == "__main__":
    app()
