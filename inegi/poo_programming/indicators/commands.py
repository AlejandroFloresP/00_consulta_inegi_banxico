import click
from indicators.services import IndicatorService
from indicators.models  import Indicator

@click.group()
def indicator():
    """Manejar el ciclo de vida de los indicadores"""
    pass


@indicator.command()
@click.option('-r', '--referencia',
              type=str,
              prompt=True,
              help= 'La referencia del indicador')
@click.option('-n', '--nombre',
              type=str,
              prompt=True,
              help= 'El nombre del indicador')
@click.option('-i', '--institucion',
              type=str,
              prompt=True,
              help= 'El nombre de la institucion')
@click.option('-d', '--descripcion',
              type=str,
              prompt=True,
              help= 'La descripción del indicador')
@click.option('-p', '--periodicidad',
              type=str,
              prompt=True,
              help= 'La periodicidad del indicador')
@click.pass_context
def create(ctx, referencia, nombre, institucion, descripcion, periodicidad):
    """Crea un nuevo indicador"""
    indicator= Indicator(referencia, nombre, institucion, descripcion, periodicidad)
    indicator_service= IndicatorService(ctx.obj['indicators_table'])
    
    indicator_service.create_indicator(indicator)


@indicator.command()
@click.pass_context
def list_ind(ctx):
    """Lista de indicadores"""
    indicator_service = IndicatorService(ctx.obj['indicators_table'])
    
    indicator_list= indicator_service.list_indicators()
    
    click.echo('Referencia  |  Nombre  |  Institucion  |  Descripcion  |  Periodicidad')
    click.echo('*' * 100)
    
    for i in indicator_list:
        click.echo('{referencia}  |  {nombre}  |  {institucion}  |  {descripcion}  |  {periodicidad}'.format(
            referencia=i['referencia'],
            nombre=i['nombre'],
            institucion=i['institucion'],
            descripcion=i['descripcion'],
            periodicidad=i['periodicidad']))


@indicator.command()
@click.pass_context
def update(ctx, client_uid):
    """Actualiza lista de indicadores"""
    pass


@indicator.command()
@click.pass_context
def delete(ctx, client_uid):
    """Elimina un indicador"""
    pass
    
    
@indicator.command()
@click.pass_context
def search_indicator(ctx, indicator_name):
    """Buscar un indicador en la lista"""
    pass


all = indicator