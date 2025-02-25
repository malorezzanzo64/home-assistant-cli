import logging

#import re
#import sys
#from typing import Any, Dict, List, Pattern  # noqa

import homeassistant_cli.autocompletion as autocompletion
#from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
import homeassistant_cli.const as const
import homeassistant_cli.helper as helper
#import homeassistant_cli.remote as api



import click
import homeassistant_cli.remote as api
from homeassistant_cli.cli import pass_context

_LOGGING = logging.getLogger(__name__)

@click.group('label')
@pass_context
def cli(ctx):
    """Get info and operate on labels from Home Assistant."""
    pass

@cli.command('list')
@click.argument('labelfilter', default=".*", required=False)
@pass_context
def listcmd(ctx: Configuration, labelfilter: str):
    """List all labels from Home Assistant."""
    ctx.auto_output("table")

    labels = api.get_labels(ctx)

    result = []  # type: List[Dict]
    if labelfilter == ".*":
        result = labels
    else:
        labelfilterre = re.compile(labelfilter)  # type: Pattern

        for label in labels:
            if labelfilterre.search(label['name']):
                result.append(label)

    cols = [('ID', 'label_id'), ('NAME', 'name')]

    ctx.echo(
        helper.format_output(
            ctx, result, columns=ctx.columns if ctx.columns else cols
        )
    )


@cli.command('add')
@click.argument('label_name')
@click.argument('label_color')
@pass_context
def add_label(ctx, label_name, label_color):
    """Add a new label."""
    frame = {
        'type': 'label/create',
        'name': label_name,
        'color': label_color
    }
    response = api.wsapi(ctx, frame)
    click.echo(response)
