import os

import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

from dataExtractor import DataExtractor

"""
Classe DataPreprocessor pour le pretraitement des donnees
"""
class DataPreprocessor () :

    """
    Constructeur de la classe DataPreprocessor
    """    
    def __init__(self, 
                 dataframe = None,
                 file_path = None, 
                 json_data = None) :
        
        if (file_path) :
            
            self.extractor = DataExtractor (file_path)
            
            self.dataframe = self.extractor.dataframe
        
        elif (dataframe is not None) :
        
            self.dataframe = dataframe
            
        elif (json_data is not None) : 
        
            self.dataframe = self.flatten_json (json_data)
        
        else :
        
            raise ValueError ("DataFrame and file path must be provided")
    """
    Methode flatten_json pour aplatir les donnees issue des colonnes du fichier JSON comme id et type
    """
    def flatten_json (self, 
                      json_data) :
        
        records = []
        
        for item in json_data ['data'] :
        
            flattened_record = {
                'id': item ['id'],
                'type': item ['type']
                }
        
            flattened_record.update (item ['attributes'])
        
            records.append (flattened_record)
        
        dataframe = pd.DataFrame (records)
        
        return dataframe
    
    """
    Methode check_data_structure pour verifier la structure des donnees
    """          
    def check_data_structure (self) :
        
        print ("\n -------------------------------------------------------------------------")
        print ("\n Checking data structure ...")
        
        if (not isinstance (self.dataframe, 
                            pd.DataFrame)) :
            
            raise TypeError (f"\n The input data is not a pandas DataFrame")
        
        if (self.dataframe.empty) :
            
            raise ValueError (f"\n The DataFrame is empty")
        
        print (f"\n DataFrame shape : {self.dataframe.shape}",
               f"\n DataFrame columns : \n {self.dataframe.columns.tolist ()} \n",
               f"\n Data types : \n {self.dataframe.dtypes} \n")
        
        print (f"\n Data structure check complete. All expected columns are present")
    
    """
    Methode clean_data pour nettoyer les donnees
    """                
    def clean_data (self) :
        
        print ("\n -------------------------------------------------------------------------")
        print ("\n Cleaning data ...")
        
        print (f"\n Missing values before cleaning : \n {self.dataframe.isna ().sum ()}")
        
        print (f"\n Type of values before cleaning : \n {self.dataframe.dtypes}")
        
        columns_to_drop = [
            'type', 
            'statusCode', 
            'currencyCode', 
            'criticality', 
            'code', 
            'codeAndDescSearch', 
            'description', 
            'serialNumber',
            'purchaseDate'
        ]
        
        for column in columns_to_drop :
            
            if (column in self.dataframe.columns) :
                
                print (f"\n Missing values in '{column}' : \n {self.dataframe [column].isna ().sum ()}")

            else :
                
                print (f"\n Column '{column}' was already deleted in dataframe")  
            
        self.dataframe = self.dataframe.drop (columns_to_drop, 
                                              axis = 1)
        
        object_columns = self.dataframe.select_dtypes (include = ['object']).columns
    
        if (len (object_columns) > 0) :
        
            print (f"\n Columns of type 'object' : {object_columns.tolist ()}")

        
        self.dataframe = self.dataframe.reset_index (drop = True)
            
        self.dataframe.dropna (axis = 1, 
                               how = 'all', 
                               inplace = True)
        
        print (f"\n Missing values after cleaning : \n {self.dataframe.isna ().sum ()}")
        
        print (f"\n Type of values after cleaning : \n {self.dataframe.dtypes}")
        
        print (f"\n Data cleaning complete")
    
    """
    Methode filter_and_replace_values pour filtrer et remplacer les valeurs
    """    
    # def filter_and_replace_values (self, 
    #                                conditions) :
        
    #     print ("\n -------------------------------------------------------------------------")
    #     print ("\n Filtering and replacing values ...")
        
    #     for column, condition in conditions.items () :
        
    #         self.dataframe.loc [condition, column] = 2009
        
    #     print ("\n Filtering and replacement complete")
    
    """
    Methode calculate_failure_probability pour calculer la probabilite de defaillance d'un equipement avec sa date 
    """                   
    def calculate_failure_probability (self) :
        
        print ("\n -------------------------------------------------------------------------")
        print ("\n Calculating failure probability ...")
        
        required_columns = ['putInServiceDate', 'life']
        
        missing_columns = [
            columns for columns in required_columns 
            if (columns not in self.dataframe.columns)]
        
        if (missing_columns) :
        
            raise ValueError (f"\n Missing required columns : {missing_columns}")
        
        # Ensure dates are converted to datetime
        for column in ['putInServiceDate', 'replacementDate', 'statusChangedDate', 'modifyDate'] :
        
            if (column in self.dataframe.columns) :
        
                self.dataframe [column] = pd.to_datetime (self.dataframe [column], 
                                                          errors = 'coerce', 
                                                          utc = True)
        
        # Compute estimated end date
        self.dataframe ['estimatedEndDate'] = self.dataframe ['putInServiceDate'] + pd.to_timedelta (self.dataframe ['life'] * 365, unit = 'D')
                        
        # Compute failure   
        current_date = pd.Timestamp.utcnow ()
        
        self.dataframe['failureProbability'] = np.where(
            current_date >= self.dataframe.apply (
                lambda row : row ['replacementDate'] + pd.to_timedelta (row ['life'] * 365, 
                                                                        unit = 'D') 
                if (pd.notnull (row ['replacementDate']))
                 
                else 
                    row ['estimatedEndDate'],
                    axis = 1
            ),
            100,
            np.clip (
                ((current_date - self.dataframe ['putInServiceDate']).dt.total_seconds () / (60 * 60 * 24 * 365)) / self.dataframe ['life'] * 100,
                0,
                100
            )
        )
        
        # Show result
        print(f"\n DataFrame with failure probability : \n {self.dataframe [['id', 'putInServiceDate', 'replacementDate', 'life', 'estimatedEndDate', 'failureProbability']].head()}")
        
        print("\n Failure probability calculation complete")
    
    """
    Methode convert_column_type pour convertir le type des colonnes en datetime
    """    
    def convert_column_type (self, 
                             new_type = 'datetime') :
        
        print ("\n -------------------------------------------------------------------------")
        
        print (f"\n Converting columns to type '{new_type}' ...")
    
        print ("\n Columns in DataFrame :\n", self.dataframe.columns.tolist())

        # Liste des colonnes à convertir
        columns_to_convert = [
            'putInServiceDate',
            'statusChangedDate',
            'replacementDate',
            'modifyDate',
            'estimatedEndDate'
        ]

        converted_columns = []

        for column in columns_to_convert :
        
            if (column in self.dataframe.columns) :
            
                if (new_type == 'datetime') :
                
                    try :
                    
                        # Convertir la colonne en datetime
                        self.dataframe [column] = pd.to_datetime (self.dataframe [column], 
                                                                  errors = 'coerce', 
                                                                  utc = True)
                    
                        print (f"\n Column '{column}' converted to type '{new_type}'")

                        # Si la colonne est bien au format datetime, la convertir en timestamp
                        if (pd.api.types.is_datetime64_any_dtype (self.dataframe [column])) :
                            
                            self.dataframe [column] = self.dataframe [column].apply (
                                
                                lambda x: x.timestamp() if pd.notnull(x) else np.nan
                            )
                        
                            print (f"\n Column '{column}' converted to float")

                        converted_columns.append(column)
                
                    except Exception as exception :
                    
                        print (f"\n Error converting column '{column}' : {exception}")

                else :
                
                    print (f"\n New type '{new_type}' is not supported")

            else :
            
                print (f"\n Column '{column}' not found in DataFrame")

        print ("\n Column conversion complete")
    
        print (f"\n Columns in DataFrame after conversion : \n {self.dataframe.dtypes}")

        return converted_columns
    
    """
    Methode convert_to_numeric pour convertir les colonnes en valeur numerique
    """    
    def convert_to_numeric (self) :
    
        print ("\n -------------------------------------------------------------------------")
        
        print ("\n Conversion columns to numeric ...")
        
        print (f"\n DataFrame before conversion : \n {self.dataframe.head()}")
        
        print (f"\n DataFrame before conversion : \n {self.dataframe.dtypes}")
        
        # Convert datetime columns to numeric (timestamps)
        datetime_columns = self.dataframe.select_dtypes(include=['datetime64']).columns
    
        for column in datetime_columns:
        
            try:
            
                self.dataframe[column] = self.dataframe[column].apply(
                    lambda x: x.timestamp() if pd.notnull(x) else np.nan
                )
            
                print(f"\n Column '{column}' converted to float")
            
            except Exception as exception:
            
                print(f"\n Error converting column '{column}': {exception}")

        # Converti les colonnes de type booleen en type floatant
        for column in self.dataframe.select_dtypes (include = ['bool']).columns:
        
            self.dataframe [column] = self.dataframe [column].astype ('float64')
        
            print (f"\n Column '{column}' converted to float64")

        # Converti la colonne "id" en type floatant
        identifier_columns = ['id']

        for column in identifier_columns:
        
            if (column in self.dataframe.columns) :
            
                label_encoder = LabelEncoder ()
            
                self.dataframe [column] = label_encoder.fit_transform(self.dataframe [column].astype (str))
            
                self.dataframe [column] = self.dataframe [column].astype ('float64')
            
                print (f"\n Column '{column}' converted to float64")

        # Converti les colonnes de type chaine de caractere (object sous python (qui equivaut au type string)) en type floatant
        for column in self.dataframe.columns:
        
            if (self.dataframe [column].dtype == 'object') :
            
                try:
                    
                    self.dataframe [column] = pd.to_numeric (self.dataframe [column], 
                                                             errors = 'raise')
            
                except ValueError as value_error :
                
                    print (f"\n Could not convert column '{column}' to numeric due to error : {value_error}")
                
                    self.dataframe [column] = pd.to_numeric (self.dataframe [column], 
                                                             errors = 'coerce')
                
                    self.dataframe [column].fillna (0, 
                                                    inplace = True)
                
                    print (f"\n No-numeric values in column '{column}' have been replaced by 0")

            
                self.dataframe [column] = self.dataframe [column].astype ('float64')
            
                print (f"\n Column '{column}' converted to float64")
        
        print (f"\n DataFrame after conversion : \n {self.dataframe.dtypes}")
        
        print (f"\n DataFrame after conversion : \n {self.dataframe.head ()}")
        
        print ("\n Conversion data complet")
    
    """
    Methode encode_categorical pour encoder les colonnes categorielles
    """   
    def encode_categorical (self) :
        
        print ("\n -------------------------------------------------------------------------")
        
        print ("\n Encoding categorical columns ...")
        
        categorical_columns = self.dataframe.select_dtypes (include = ['object']).columns
        
        if (len (categorical_columns) == 0) :
        
            print ("\n No categorical columns to encode")
        
            return
        
        print (f"\n Categorical columns to encode : {categorical_columns.tolist ()}")
        
        for column in categorical_columns:
            
            unique_columns = self.dataframe [column].nunique ()
            
            # Si le nombre unique de valeurs est faible, on utilise le Label Encoding
            if (unique_columns < 5) :
                
                labelEncoder = LabelEncoder ()
        
                self.dataframe [column] = labelEncoder.fit_transform (self.dataframe [column].astype (str))
        
                print (f"\n Column '{column}' encoded with Label Encoding")
        
            else:
        
                # Si pour labelEncoder le nombre de valeurs unique est élevé, on utilise le One-Hot Encoding
                self.dataframe = pd.get_dummies (self.dataframe, 
                                                 columns = [column], 
                                                 prefix = [column],
                                                 drop_first = True)
        
                print (f"\n Column '{column}' encoded with One-Hot Encoding")
        
        print (f"\n Data after encoding : \n {self.dataframe.head ()}")
        
        print (f"\n Data encoding complete")
    
    """
    Methode impute_data pour imputer les donnees manquantes
    """    
    def impute_data (self, 
                     strategy = 'mean') : 
        
        print ("\n -------------------------------------------------------------------------")
        print (f"\n Imputing missing values using strategy : {strategy}")
        
        numerical_columns = self.dataframe.select_dtypes(include=['float64', 'int64']).columns
        
        print (f"\n Numerical columns for imputation : {numerical_columns.tolist ()}")
        
        if (len (numerical_columns) > 0) :
        
            imputer = SimpleImputer (strategy = strategy)
        
            self.dataframe [numerical_columns] = imputer.fit_transform (self.dataframe [numerical_columns])
        
        print ("\n Imputation complete")
    
    """
    Methode normalize_data pour normaliser les donnees brutes si necessaire
    """    
    # def normalize_data (self) :
        
    #     print ("\n -------------------------------------------------------------------------")
    #     print ("\n Normalizing data ...")
                
    #     numerical_columns = self.dataframe.select_dtypes(include=['float64', 'int64']).columns
        
    #     print (f"\n Data before normalization: \n {self.dataframe[numerical_columns].head()}")
                        
    #     if (len (numerical_columns) > 0) :
            
    #         scaler = StandardScaler ()
             
    #         try :
            
    #             self.dataframe [numerical_columns] = scaler.fit_transform (self.dataframe [numerical_columns])
        
    #             print(f"\n Data after normalization : \n {self.dataframe [numerical_columns].head ()}")
        
    #         except ValueError as exception :
            
    #             print (f"\n Error : Could not normalize data",
    #                    f"\n {str (exception)}")
        
    #     print ("\n Data normalization complete")
    
    """
    Methode save_dataframe_csv pour sauvegarder les donnees dans un fichier CSV
    """    
    def save_dataframe_csv (self, 
                            file_name, 
                            directory_path = '../dataCSV/', 
                            separator = ',', 
                            encoding = 'utf-8', 
                            include_index = False) :
        
        try :
            
            full_path = f"{directory_path}{file_name}"
            
            if (os.path.exists (full_path)) :
                
                print(f"\n File '{file_name}' already exist in '{directory_path}'.")
            
                return
            
            self.dataframe.to_csv (full_path, 
                                   sep = separator, 
                                   encoding = encoding, 
                                   index = include_index)
            
            print (f"\n File '{file_name}' was registred with sucess in '{directory_path}'")
            
        except Exception as exception :
            
            print (f"\n Error save : {exception}")
    
    """
    Methode preprocess_data pour pretraiter les donnees
    """            
    def preprocess_data (self, 
                         dataframe = None,
                         missing_strategy = 'mean',
                         output_file_name = 'train.csv', 
                         output_directory = '../dataCSV/') :
        
        print ("\n Starting data preprocessing ...")
        
        try :
        
            self.check_data_structure ()
        
            self.clean_data ()
            
            self.calculate_failure_probability ()
            
            self.convert_column_type (new_type = 'datetime')
            
            self.convert_to_numeric ()
            
            self.encode_categorical ()
            
            self.impute_data (strategy = missing_strategy)
            
            # self.normalize_data ()
            
            self.save_dataframe_csv (file_name = output_file_name, 
                                     directory_path = output_directory)
            
            print ("\n Data preprocessing complete")
            
        except Exception as exception :
        
            print (f"Error in preprocessing data : {exception}")
        
            dataframe = self.dataframe
        
        return dataframe