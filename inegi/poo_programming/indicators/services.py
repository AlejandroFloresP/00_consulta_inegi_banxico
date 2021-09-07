import csv, os
from indicators.models  import Indicator


class IndicatorService:
    
    def __init__(self, table_name):
        self.table_name = table_name
        
    def create_indicator(self, indicator):
        with open(self.table_name, mode='a', encoding='latin-1') as f:
            writer= csv.DictWriter(f, fieldnames=Indicator.schema())
            writer.writerow(indicator.to_dict())
    
    def list_indicators(self):
        with open(self.table_name, mode='r', encoding='latin-1') as f:
            reader = csv.DictReader(f, fieldnames=Indicator.schema())
            
            return list(reader)
    
    def update_indicator_metadata(self, update_indicator):
        indicators= self.list_indicators()
        
        updated_indicators = []
        for idx, indicator in enumerate(indicators):
            if idx == update_indicator:
                updated_indicators.append(update_indicator.to_dict())
            else:
                updated_indicators.append(indicator)
        
        self._save_to_disk(updated_indicators)
        
    def _save_to_disk(self, update_indicators):
        tmp_table_name= self.table_name + '.tmp'
        with open(tmp_table_name, mode='w', encoding='latin-1') as f:
            writer = csv.DictWriter(f, fieldnames=Indicator.schema())
            writer.writerows(update_indicators)
            
            os.remove(self.table_name)
            os.rename(tmp_table_name, self.table_name)
            
        