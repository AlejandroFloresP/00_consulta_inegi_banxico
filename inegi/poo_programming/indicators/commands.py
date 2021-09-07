import click
from indicators.services import IndicatorService
from indicators.models  import Indicator
from tabulate import tabulate

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
    
    headers = [field.capitalize() for field in Indicator.schema()]
    table = []
    
    for idx, indicator in enumerate(indicator_list):
        table.append(
            [idx,
             indicator['referencia'],
             indicator['nombre'],
             indicator['institucion'],
             indicator['descripcion'],
             indicator['periodicidad']])

    print(tabulate(table, headers))

@indicator.command()
@click.argument('indicator_referencia')
@click.pass_context
def update(ctx, indicator_referencia):
    """Actualiza lista de indicadores"""
    indicator_service = IndicatorService(ctx.obj['indicators_table'])
    
    indicator_list = indicator_service.list_indicators()        
    
    indicator = [indicator for indicator in indicator_list if indicator['referencia'] == indicator_referencia]
    
    if indicator:
        click.echo(indicator)
        indicator = _update_indicator_flow(Indicator(**indicator[0]))
        indicator_service.update_indicator_metadata(indicator)
    else:
        click.echo('Indicador no encontrado')
        
    
def _update_indicator_flow(indicator):
    click.echo('Deja vacio si no quieres modificar el valor')
    
    indicator.referencia = click.prompt('Nueva referencia', default = indicator.referencia)
    indicator.nombre = click.prompt('Nuevo nombre', default = indicator.nombre)
    indicator.institucion = click.prompt('Nueva institucion', default = indicator.institucion)
    indicator.descripcion = click.prompt('Nueva descripcion', default = indicator.descripcion)
    indicator.periodicidad = click.prompt('Nueva periodicidad', default = indicator.periodicidad)
    
    return indicator


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