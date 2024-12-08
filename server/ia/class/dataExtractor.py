import json
import pandas as pd

"""
Classe DataExtractor pour extraire les donnees
"""
class DataExtractor () :

    """
    Constructeur de la classe DataExtractor
    """    
    def __init__(self, 
                 file_path_json) :
    
        self.file_path_json = file_path_json
    
        self.data = self.load_json ()
        
        self.dataframe = self.convert_dataframe ()
    
    """
    Methode load_json pour charger les donnees du fichier JSON
    """
    def load_json (self) :
    
        print ("\n -------------------------------------------------------------------------")
        print (f"\n Loading data from JSON file : {self.file_path_json} ...")
        
        try : 
        
            with open (self.file_path_json, 'r') as file :
    
                data = json.load (file)
            
            print (f"\n Data loaded from JSON file")
            
            return data
        
        except FileNotFoundError :
            
            print (f"\n Error: The file {self.file_path_json} was not found")
            
            return None
        
        except json.JSONDecodeError as exception :
        
            print(f"\n Error failed to decode JSON file : \n {str (exception)}")
        
            return None
        
        except Exception as exception :
        
            print(f"\n Error an unexpected error occurred {str (exception)}")
        
            return None
    
    """
    Methode convert_dataframe pour convertir les donnees JSON en DataFrame
    """     
    def convert_dataframe (self) :
        
        print ("\n -------------------------------------------------------------------------")
        print (f"\n Convert JSON data in dataframe ...")
        
        try :
            
            if ('data' in self.data) :
            
                records = []
            
                for item in self.data ['data'] :
            
                    flattened_record = {
                        'id': item ['id'], 
                        'type': item ['type']
                        }
            
                    flattened_record.update (item['attributes'])
            
                    records.append (flattened_record)
            
                dataframe = pd.DataFrame (records)
            
            else :
            
                dataframe = pd.json_normalize (self.data, 
                                               sep = '_', 
                                               max_level = 1)
        
            print (f"\n DataFrame shape : {dataframe.shape}")
        
            print (f"\n DataFrame columns : \n {dataframe.columns.tolist ()}")
        
            return dataframe
    
        except Exception as exception :
            
            print (f"\n Error: Failed to convert JSON data to DataFrame {str(exception)}")
            
            return None
    
    """
    Methode extract_columns pour extraire les colonnes du DataFrame
    """
    def extract_columns (self) :
        
        if (self.dataframe is None) :
            
            print (f"\n Error: No DataFrame available to extract columns from")
            
            return []
        
        columns = list (self.dataframe.columns)
        
        return columns