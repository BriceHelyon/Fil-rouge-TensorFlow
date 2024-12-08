import json
import requests

import pandas as pd

"""
Classe RequestAPI pour effectuer des requetes API sur le client    
"""
class RequestAPI () :
    
    """
    Constructeur de la classe RequestAPI
    """
    def __init__(self, 
                 login_url, 
                 api_url, 
                 credentials) :
        
        self.login_url = login_url
        self.api_url = api_url
        self.credentials = credentials
        self.token = None
    
    """
    Methode get_token pour recuperer le token d'authentification
    """
    def get_token (self) :
        
        try :
            
            response = requests.post (self.login_url, 
                                      data = self.credentials)
            
            response.raise_for_status ()
            
            self.token = response.json ().get ('X-CS-Access-Token')
            
            if (not self.token) :
                
                raise Exception ("Token not found in the response")
            
            print (f"X-CS-Access-Token : {self.token}")
            
            return self.token
        
        except requests.exceptions.HTTPError as http_err :
            
            raise Exception (f"HTTP error occurred : {http_err}")
        
        except Exception as err :
            
            raise Exception (f"An error occurred : {err}")
    
    """
    Methode call_api_with_token pour effectuer des requetes API avec le token d'authentification
    """
    def call_api_with_token (self) :
        
        if (not self.token) :
            
            self.get_token ()
        
        try :
            
            headers = {
                'X-CS-Access-Token': self.token,  # Utiliser 'X-CS-Access-Token' pour l'authentification
                'Content-Type': 'application/json'  # En-tête supplémentaire pour le type de contenu attendu
            }
            
            response = requests.get (self.api_url, 
                                     headers = headers)

            response.raise_for_status ()

            return response.json ()
        
        except requests.exceptions.HTTPError as http_err :
            
            raise Exception (f"HTTP error occurred : {http_err}")
        
        except Exception as err :
            
            raise Exception (f"An error occurred : {err}")
    
    """
    Methode fetch_and_save_json pour recuperer et sauvegarder les donnees du fichier JSON
    """
    def fetch_and_save_json (self, 
                             file_path_json) :
        
        try :
            
            json_data = self.call_api_with_token ()
            
            # print (f"JSON Data fetched : {json_data}")
            
            with open (file_path_json, 'w') as file :
                
                json.dump (json_data, 
                           file, 
                           indent = 4)
            
            print (f"\n Data fetched and saved successfully to {file_path_json}")
        
        except Exception as exception :
            
            raise Exception (f"Error fetching data : \n {str (exception)}")
    
    """
    Methode json_to_dataframe pour convertir les donnees du fichier JSON en dataframe
    """
    def json_to_dataframe (self, 
                           json_data) :
        
        print (f"\n Inspecting JSON Data Structure : {json_data}")
        
        if (isinstance (json_data, list)) :
            
            dataframe = pd.DataFrame (json_data)
            
            return dataframe
        
        else :
            
            raise ValueError ("JSON data is not a list of dictionaries")