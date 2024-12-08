import psycopg2 # type: ignore
import pandas as pd

"""
Classe DataBase pour la connexion et l'insertion des donnees dans la base de donnees PGSQL
"""
class DataBase :

    """
    Constructeur de la classe DataBase
    """
    def __init__(self, 
                 database_config) :

        self.host = database_config ['host']
        self.dbname = database_config ['dbname']
        self.user = database_config ['user']
        self.password = database_config ['password']
        self.connection = None
        
    """
    Methode connect pour se connecter a la base de donnees PGSQL
    """
    def connect (self) :

        try :

            self.connection = psycopg2.connect(
                host = self.host,
                dbname = self.dbname,
                user = self.user,
                password = self.password
            )

            print ("Connection successfully to the database PGSQL")

        except (Exception, psycopg2.DatabaseError) as error :

            print (f"Error connection : {error}")

    """
    Methode insert_csv_data pour inserer les donnees issue du fichier CSV (predictions) dans la base de donnees PGSQL
    
    utilisation de cursor pour parcourir les resultat
    """
    def insert_csv_data (self, 
                         csv_file, 
                         table_name) :

        try :
            
            data = pd.read_csv (csv_file)

            cursor = self.connection.cursor ()

            columns = ', '.join(data.columns)
            
            placeholders = ', '.join(['%s'] * len (data.columns))
            
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            for row in data.itertuples (index = False, 
                                        name = None) :
                
                cursor.execute (insert_query, 
                                row)

            self.connection.commit ()

            print(f"Insert data in the table {table_name}")

        except (Exception, psycopg2.DatabaseError) as error :
            
            print (f"Insert error during the data insert : {error}")
            
            if (self.connection) :
            
                self.connection.rollback ()
        
        finally :
            
            if (self.connection) :
            
                cursor.close ()
                
    """
    Methode close pour fermer la connexion a la base de donnees PGSQL
    """
    def close (self) :
        
        if (self.connection) :

            self.connection.close ()

            print ("Close connexion.")