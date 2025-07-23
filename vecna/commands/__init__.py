import typer

from .credentials import app as credentials_app
from .init import app as init_app
from .lock import app as lock_app
from .unlock import app as unlock_app
from .version import app as version_app

app = typer.Typer()

app.add_typer(version_app)
app.add_typer(init_app)
app.add_typer(unlock_app)
app.add_typer(lock_app)
app.add_typer(
    credentials_app,
    name="creds",
)
