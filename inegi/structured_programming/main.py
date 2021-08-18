import os, requests, sys, csv, json, datetime
import pandas as pd

INDICATOR_TABLE = 'indicators.csv'
INDICATOR_SCHEMA = ['referencia', 'nombre', 'institucion', 'descripcion', 'periodicidad']
indicators = []

def _initialize_indicators_from_storage():
    with open(INDICATOR_TABLE, mode='r',  encoding='latin-1') as f:
        reader = csv.DictReader(f, fieldnames=INDICATOR_SCHEMA)
        
        for row in reader:
            indicators.append(row)


def _save_indicators_to_storage():
    tmp_table_name = '{}.tmp'.format(INDICATOR_TABLE)
    
    with open(tmp_table_name, mode = 'w') as f:
        writer = csv.DictWriter(f, fieldnames = INDICATOR_SCHEMA)
        writer.writerows(indicators)
        
        os.remove(INDICATOR_TABLE)
        f.close()
        os.rename(tmp_table_name, INDICATOR_TABLE)


# def update_indicator()
        
def create_indicator(indicator):
    global indicators
    
    if indicator not in indicators:
        indicators.append(indicator)
    else:
        print('Indicador ya esta en la lista')


def list_indicators():
    print('ID | Referencia | Nombre | Institucion | Descripcion | Periodicidad')
    print('-'*50)
    
    for idx, indicator in enumerate(indicators):
        print('{id} | {referencia} | {name} | {institution} | {description} | {periodicity}'.format(
            id = idx,
            referencia = indicator['referencia'],
            name = indicator['nombre'],
            institution = indicator['institucion'],
            description = indicator['descripcion'],
            periodicity = indicator['periodicidad']
    ))


def update_indicator(indicator_id, update_indicator_info):
    global indicators
    
    if len(indicators) -1 >= indicator_id:
        indicators[indicator_id] = update_indicator_info
    else:
        print('El indicador no está en la lista')


def delete_indicator(indicator_id):
    global indicators

    for idx, indicator in enumerate(indicators):
        if idx == indicator_id:
            del indicators[idx]
            break


def search_indicator(indicator_name):
    for indicator in indicators:
        if indicator['nombre'] != indicator_name:
            continue
        else:
            return True

def consult_indicator(reference):
    url='https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'+reference+'/es/0700/false/BIE/2.0/490dcd21-44b2-fef6-0ade-e6431a8c8fb9?type=json'
    response = requests.get(url)
    
    if response.status_code==200:
        content = json.loads(response.content)
        Series = content['Series'][0]['OBSERVATIONS']
        
        dato_obs=[]
        fecha= []
        
        for obs in Series:
            dato_obs.append(float(obs['OBS_VALUE']))
            
        for obs in Series:
            fecha.append((obs['TIME_PERIOD']))
        
        df= pd.DataFrame(list(zip(fecha,dato_obs)), columns=['Fecha', reference])
        
    return df


def _get_indicator_field(field_name, message='¿Cuál es el {} del indicador?'):
    field = None
    
    while not field: 
        field = input(message.format(field_name))
    
    return field


def _get_indicator():
    indicator = {
        'referencia': _get_indicator_field('referencia'),
        'nombre': _get_indicator_field('nombre'),
        'institucion': _get_indicator_field('institucion'),
        'descripcion': _get_indicator_field('descripcion'),
        'periodicidad': _get_indicator_field('periodicidad'),
    }

    return indicator


def _print_welcome():
    print('Bienvenidos al programa para la consulta de indicadores del SAT')
    print('-'*50)
    print('¿Qué te gustaria hacer hoy?')
    print('1. Actualizar indicadores')
    print('2. Añadir indicador')
    print('3. Buscar indicador en la lista')
    print('4. Consultar indicador')
    print('5. Eliminar indicador de la lista')
    print('6. Ver lista de indicadores')


if __name__ == '__main__':
    _initialize_indicators_from_storage()
    _print_welcome()
    
    command = input()
    
    if command == '1':
        indicator_id = int(_get_indicator_field('id'))
        update_indicator_info = _get_indicator()
        
        update_indicator(indicator_id, update_indicator_info)
    elif command == '2':
        indicator = _get_indicator()

        create_indicator(indicator)
    elif command == '3':
        indicator_name = _get_indicator_field('nombre')
        found = search_indicator(indicator_name)

        if found:
            print('El indicador, {}, esta en la lista de indicadores'.format(indicator_name))
        else:
            print('El indicador, {}, no esta en la lista de indicadores'.format(indicator_name))
    elif command == '4':
        reference = _get_indicator_field('referencia')
        
        df = consult_indicator(reference)

        df.to_excel('{}'.format(reference))
    elif command == '5':
        indicator_id = int(_get_indicator_field('id'))

        delete_indicator(indicator_id)
    elif command == '6':
        list_indicators()
    else:
        print('Comando invalido')
    
    _save_indicators_to_storage()

