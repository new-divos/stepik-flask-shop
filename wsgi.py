#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from flask.cli import FlaskGroup

from app import create_app, db
from app.config import config


current_config = config.get(os.getenv('FLASK_ENV'))
if current_config is None:
    raise RuntimeError(
        "Unknown configuration: check FLASK_ENV environment variable value"
    )

app = create_app(current_config)
cli = FlaskGroup(app)


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db
    )


if __name__ == '__main__':
    cli()