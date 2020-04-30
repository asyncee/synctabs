#!/usr/bin/env python

import typer

from synctabs.presentation.cli.add_user import add_user

app = typer.Typer()
app.command("add_user")(add_user)

app.callback()(lambda: None)


if __name__ == "__main__":
    app()
