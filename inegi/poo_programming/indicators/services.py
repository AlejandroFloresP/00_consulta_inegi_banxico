import csv
from indicators.models  import Indicator


class IndicatorService:
    
    def __init__(self, table_name):
        self.table_name = table_name
        
    def create_indicator(self, indicator):
        with open(self.table_name, mode='a', encoding='latin-1') as f:
            writer= csv.DictWriter(f, fieldnames=Indicator.schema())
            writer.writerow(indicator.to_dict())
    
    def list_indicators(self):
        with open(self.table_name, mode='r') as f:
            reader = csv.DictReader(f, fieldnames=Indicator.schema())
            
            return list(reader)