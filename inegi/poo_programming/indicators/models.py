import uuid

class Indicator:
    
    def __init__(self, referencia, nombre, institucion, descripcion, periodicidad):
        self.referencia = referencia
        self.nombre = nombre
        self.institucion = institucion
        self.descripcion = descripcion
        self.periodicidad = periodicidad
    
    def to_dict(self):
        return vars(self)
    
    @staticmethod
    def schema():
        return ['referencia', 'nombre', 'institucion', 'descripcion', 'periodicidad']