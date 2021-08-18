import click

from indicators import commands as indicator_commands

INDICATOR_TABLE= '00_data/indicators.csv'


@click.group()
@click.pass_context
def ind(ctx):
    ctx.obj = {}
    ctx.obj['indicators_table'] = INDICATOR_TABLE


ind.add_command(indicator_commands.all)