import typer

from .version import app as version_app
from .init import app as init_app
from .unlock import app as unlock_app

app = typer.Typer()

app.add_typer(version_app)
app.add_typer(init_app)
app.add_typer(unlock_app)
