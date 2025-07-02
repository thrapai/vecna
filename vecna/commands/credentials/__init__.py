import typer

from .add import app as add_app
from .get import app as get_app


app = typer.Typer()

app.add_typer(add_app)
app.add_typer(get_app)
