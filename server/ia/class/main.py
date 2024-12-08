import os
import time
import warnings

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras import Sequential # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore
from tensorflow.keras.losses import MeanSquaredError # type: ignore
from tensorflow.keras.metrics import MeanAbsoluteError # type: ignore
from tensorflow.keras.layers import Dense, Conv1D, LSTM # type: ignore
from statsmodels.tsa.arima.model import ARIMA # type: ignore

warnings.filterwarnings('ignore')

from requestAPI import RequestAPI
from dataPreprocessor import DataPreprocessor
from dataExtractor import DataExtractor
from dataWindow import DataWindow
# from dataBase import DataBase

"""
Classe Main pour lancer le programme
"""
class Main :
    
    """
    Constructeur de la classe Main
    """  
    def __init__(self, 
                 batch_size = 32) :
        
        plt.rcParams['figure.figsize'] = (10, 7.5)
        plt.rcParams['axes.grid'] = False

        print (f"TensorFlow version : {tf.__version__}")

        """
        Initialisation des seeds pour la reproductibilite des resultats
        """
        tf.random.set_seed (42)
        np.random.seed (42)
        
        """
        Initialisation des variables pour l'API du client
        """
        self.login_url = "https://lhsm-v7-acceptance.carl-source.com/gmaoCS04/api/auth/v1/authenticate"
        self.api_url = "https://lhsm-v7-acceptance.carl-source.com/gmaoCS04/api/entities/v1/material?page[offset]=0&page[limit]=300"
        #limite définie à 1 pour les tests il faudra remettre 300 à la fin 
        self.credentials = {
            'login': 'BAILHACHE-R',
            'password': 'Bailhache2024$.',
            'origin': 'Postman_SCA'
        }
        
        self.raw_file_path = '../dataJSON/raw.json'
        self.train_file_path = '../dataCSV/train.csv'
        self.prediction_file_path = '../dataCSV/predictions.csv'
        
        self.train_dataframe = None
        
        self.load_or_fetch_data ()
        
        if (self.train_dataframe is None) :
            
            raise ValueError ("Failed to initialize. Check data fetching process")
        
        self.column_indices = {
            name: i for i, name in enumerate (self.train_dataframe.columns)
        }
        
        """
        Initialisation des variables pour la fenetre de donnees
        """
        self.OUT_STEPS = 24
        self.batch_size = batch_size
        
        self.multiple_window = DataWindow (input_width = 10, 
                                           label_width = 10, 
                                           shift = 1, 
                                           train_dataframe = self.train_dataframe,
                                           label_columns = ['estimatedEndDate', 
                                                            'failureProbability'], # mettre les 15 colonnes
                                           batch_size = self.batch_size)
        
        self.validation_performance = {}
        self.performance = {}
    
    """
    Fonction qui extrait les donnees de l'API du client
    """    
    def fetch_data_from_api (self) :
        
        try :
            
            request_API_client = RequestAPI (self.login_url, 
                                             self.api_url, 
                                             self.credentials)
            
            request_API_client.fetch_and_save_json (self.raw_file_path)
            
            print ("Data fetched from API and saved successfully")
            
            data_extractor = DataExtractor (self.raw_file_path)
            
            if (data_extractor.dataframe is not None) :
            
                self.train_dataframe = data_extractor.dataframe
            
            else :
                
                raise ValueError ("DataExtractor failed to create a DataFrame")
            
        except Exception as exception :
            
            self.train_dataframe = None
            
            print (f"Error fetching data : \n {str (exception)}")
    
    """
    Fonction qui charge les donnees si le fichier existe sinon les extrait de l'API du client
    """    
    def load_or_fetch_data (self) :
        
        try :
        
            if (os.path.exists (self.train_file_path)) :
                
                print (f"\n Train file found at {self.train_file_path}, loading data ...")
                
                self.wait_for_file(self.train_file_path, timeout=120)
                
                try:
                
                    self.train_dataframe = pd.read_csv(self.train_file_path)
                
                    print (f"\n Data loaded successfully from {self.train_file_path}")
                
                    return
        
                except Exception as exception :
        
                    print (f"\n Error loading train file : {str (exception)}")
                    
                    self.fetch_data_from_api ()
        
            else:
                
                print (f"\n Train file not found \n", 
                       f"Proceeding with data extraction from {self.raw_file_path} ...")
        
            data_extractor = DataExtractor (self.raw_file_path)
        
            if (data_extractor.dataframe is not None) :
            
                self.train_dataframe = data_extractor.dataframe
            
                print (f"\n Successfully loaded raw data from {self.raw_file_path}")
        
            else :
                
                raise ValueError ("\n DataExtractor failed to create a DataFrame")
        
        except (FileNotFoundError, ValueError) as error :
            
            print (f"\n Error: {str (error)}")
        
            print (f"\n File {self.raw_file_path} not found")
        
            self.fetch_data_from_api ()
        
            if (self.train_dataframe is not None) :
            
                print (f"\n Fetching data from API was successful")
            
            else :
            
                print (f"\n Failed to fetch data from API")
            
                raise ValueError ("\n Data could not be fetched from API")
    
    """
    Fonction qui pretraite les donnees
    """    
    def dataPreprocessor (self) :
        
        print ("\n -------------------------------------------------------------------------")
        
        print (f"\n Running Preprocessor")
            
        if (self.train_dataframe is None) : 
            
            print (f"\n Error : DataFrame is not initialized")
            
            return
            
        data_preprocessor = DataPreprocessor (dataframe = self.train_dataframe)
        
        try :
        
            print (f"Data before preprocessing : \n {self.train_dataframe.head ()} \n")
        
            data_preprocessor.check_data_structure ()
         
            data_preprocessor.preprocess_data (missing_strategy = 'mean')   
            
        except Exception as exception :
        
            print (f"Error during preprocessing : {exception}")
        
            return

        if (data_preprocessor.dataframe is None) :
            
            print ("Error : Preprocessed DataFrame is None")
        
            return
        
        self.train_dataframe = data_preprocessor.dataframe
        
        print (f"\n Data after preprocessing : \n {self.train_dataframe.head ()}")
        
        print (f"\n Train dataframe shape : \n {self.train_dataframe.shape}")
    
    """
    Fonction qui attend la creation d'un fichier
    """    
    def wait_for_file (self, 
                       file_path, 
                       timeout = 60, 
                       delay = 2) :
    
        start_time = time.monotonic()
    
        while (not os.path.isfile (file_path)) :
        
            if (time.monotonic () - start_time > timeout) :
            
                raise TimeoutError (f"\n File {file_path} not found within timeout period.")
        
            time.sleep (delay)

        while (os.path.getsize (file_path) == 0) :

            if (time.monotonic () - start_time > timeout) :
    
                raise TimeoutError(f"\n File {file_path} is empty after timeout period.")
        
            time.sleep (delay)
            
        previous_size = 0
        
        while (True) :
        
            current_size = os.path.getsize (file_path)
        
            if (current_size == previous_size) :
        
                break
        
            previous_size = current_size
        
            time.sleep (delay)
    
    """
    Fonction qui cree une fenetre de donnees pour l'entrainement, la validation et le test
    """    
    def create_print_data_window (self) :
        
        window = DataWindow (input_width = 10, 
                             label_width = 10, 
                             shift = 1,
                             train_dataframe = self.train_dataframe,
                             label_columns = ['id',
                                              'xtraTxt02',
                                              'xtraTxt03',
                                              'residualPr',
                                              'xtraNum02',
                                              'referMaterial',
                                              'toScrap',
                                              'putInServiceDate',
                                              'statusChangedDate',
                                              'replacementDate',
                                              'modifyDate',
                                              'life',
                                              'reparable',
                                              'estimatedEndDate',
                                              'failureProbability'],
                             batch_size = self.batch_size)
        
        print ("\n -------------------------------------------------------------------------")
        
        print (f'\n Window train : \n {window.train} \n', 
               f'\n Window validation : \n {window.validation} \n',
               f'\n Window test : \n {window.test} \n')
        
        print (f"Window number batches train : {window.train_batches} \n",
               f"\n Window number batches validation : {window.validation_batches} \n",
               f"\n Window number batches test : {window.test_batches}")

    """
    Fonction qui divise le dataframe en deux parties : entrainement et validation
    """
    def train_test_split (self, 
                          dataframe, 
                          test_size = 0.2) :
        
        n = len (dataframe)
        
        train_dataframe = dataframe [:int (n * (1 - test_size))]
        validation_dataframe = dataframe [int (n * (1 - test_size)):]
        
        return train_dataframe, validation_dataframe
    
    """
    Fonction qui compile et entraine le modele avec des hyperparametres
    
    patience = nombre d'epoque
    max_epochs = nombre d'epoque
    early_stopping = anticipe l'arret du nombre d'epoque (patience)
    
    Methode model.compile = evalue la performance du modele (écart entre la valeur réelle et prédicte)
    
    Variable history = montre les performances du modele pour chaque epoque d'entrainement
    """
    def compile_and_fit(self, 
                        model, 
                        window, 
                        patience = 3, 
                        max_epochs = 11) :
        
        print (f"\n Training model : {model.name} \n")
        
        early_stopping = EarlyStopping (monitor = 'val_loss', 
                                        patience = patience, 
                                        mode = 'min')
        
        model.compile(loss = MeanSquaredError (), 
                      optimizer = Adam (), 
                      metrics = [MeanAbsoluteError ()])
        
        print (f"\n Model summary : {model.summary ()}")
        
        print (f"\n Starting training for {max_epochs} epochs ...")
        
        history = model.fit(window.train, 
                            epochs = max_epochs, 
                            validation_data = window.validation, 
                            callbacks = [early_stopping])
        
        return history

    """
    modèle classique DENSE pour voir la différence des valeurs prédictes avec des modèles hybride pour des séries temporelles
    """
    # def dense_model (self):

    #     print ("\n -------------------------------------------------------------------------")
    #     print ("Running Dense Model")
        
    #     try :

    #         self.wait_for_file (self.train_file_path, timeout=120)
    #         data = pd.read_csv (self.train_file_path)
            
    #         print(f"\n Data loaded successfully from {self.train_file_path}")

    #         dense = Sequential([
    #             Dense (32, activation = 'relu'),
    #             Dense (32, activation = 'relu'),
    #             Dense (15, kernel_initializer = tf.initializers.zeros),
    #         ])
        
    #         self.compile_and_fit(dense, 
    #                              self.multiple_window)
        
    #         self.validation_performance ['Dense'] = dense.evaluate (self.multiple_window.validation)
        
    #         print (f"\n Validation performance : {self.validation_performance} \n")
        
    #         self.performance ['Dense'] = dense.evaluate (self.multiple_window.test, 
    #                                                      verbose = 0)

    #         print (f"Test performance : {self.performance}")

    #         self.multiple_window.plot(dense_model)
            
    #         plt.savefig('../figures/DENSE.png', dpi=300)

    #     except TimeoutError as timeOutError:
        
    #         print(f"\n Error waiting for file train : {str(timeOutError)}")

    #     except Exception as exception:
            
    #         print(f"\n Error running ARIMA-LSTM model : \n {str(exception)}")
    
    """
    modèle hybride ARIMA_LSTM pour voir la dofférence des valeurs pré dites avec les autres modèles classique pour des séries temporelles
    """
    # def arima_lstm_model(self):
        
    #     print("\n -------------------------------------------------------------------------")
    #     print("\n Running ARIMA-LSTM Model")

    #     try:
    #         self.wait_for_file (self.train_file_path, timeout=120)
    #         data = pd.read_csv (self.train_file_path)
            
    #         print(f"\n Data loaded successfully from {self.train_file_path}")

    #         # Fit ARIMA model
    #         arima_model = ARIMA(data, order=(p, d, q))  # Définir les paramètres p, d, q
    #         arima_fit = arima_model.fit()
            
    #         print (f"\n ARIMA Model Summary:\n {arima_fit.summary()}")

    #         # Préparez les données pour LSTM, en utilisant les résidus ARIMA
    #         residuals = arima_fit.resid
        
    #         # Transformation des données pour LSTM
    #         lstm_model = Sequential([
    #             LSTM(32, return_sequences=True, input_shape = (10, 15)),
    #             Dense(15, kernel_initializer = tf.initializers.zeros)
    #         ])

    #         print(f"\n Compiling and fitting model ...")
        
    #         self.compile_and_fit(lstm_model, self.multiple_window)

    #         # Évaluation et prédictions
    #         self.validation_performance['ARIMA-LSTM'] = lstm_model.evaluate(self.multiple_window.validation)
        
    #         print(f"\n Validation performance : {self.validation_performance} \n")

    #         self.performance['ARIMA-LSTM'] = lstm_model.evaluate(self.multiple_window.test, verbose=0)
            
    #         print(f"Test performance : {self.performance}")

    #         self.multiple_window.plot(lstm_model)
            
    #         plt.savefig('../figures/ARIMA_LSTM.png', dpi=300)

    #     except TimeoutError as timeOutError:
        
    #         print(f"\n Error waiting for file train : {str(timeOutError)}")

    #     except Exception as exception:
            
    #         print(f"\n Error running ARIMA-LSTM model : \n {str(exception)}")

    """
    Fonction qui execute le modele LSTM
    
    modèle classique LSTM pour voir la différence des valeurs prédictes avec un modèle hybride pour des séries temporelles
    adapter ce code aux autres modèles pour réaliser des tests sur un modèle en particulier pour comparer les performances en changeant la partie lstm_model = ...
    """
    def lstm_model (self) :
        
        print ("\n -------------------------------------------------------------------------")
        print ("\n Running LSTM Model")
        
        try : 
            
            self.wait_for_file (self.train_file_path, 
                                timeout = 120)
                    
            data = pd.read_csv (self.train_file_path)
            
            print (f"\n Data loaded successfully from {self.train_file_path}")
                                 
            lstm_model = Sequential ([
                LSTM (32, return_sequences = True, input_shape = (10, 15)),
                Dense (15, kernel_initializer = tf.initializers.zeros),
            ])
            
            print (f"\n Compiling and fitting model ...")
            
            self.compile_and_fit(lstm_model, 
                                self.multiple_window)
            
            self.validation_performance ['LSTM'] = lstm_model.evaluate (self.multiple_window.validation)
            
            print (f"\n Validation performance : {self.validation_performance} \n")
            
            self.performance ['LSTM'] = lstm_model.evaluate (self.multiple_window.test, 
                                                            verbose = 0)
            
            print (f"Test performance : {self.performance}")
            
            self.multiple_window.plot (lstm_model)
            
            plt.savefig ('../figures/LSTM.png', 
                        dpi = 300)
            
            validation_predictions = lstm_model.predict (self.multiple_window.validation)
            
            test_predictions = lstm_model.predict (self.multiple_window.test)
            
            self.save_predictions (validation_predictions, 
                                   test_predictions)
            
        except TimeoutError as timeOutError :
            
            print (f"\n Error waiting for file train : {str (timeOutError)}")

        except Exception as exception :
            
            print (f"\n Error running LSTM model : \n {str (exception)}")

    """
    Fonction qui sauvegarde les predictions dans un fichier CSV nomme validation et test et envoi les donnees dans une base de donnees PGSQL
    """
    def save_predictions (self, 
                          validation_predictions, 
                          test_predictions) :
    
        try :
        
            validation_predictions_df = pd.DataFrame (validation_predictions, 
                                                      columns = ['id', 
                                                                 'estimatedEndDate'])
            
            test_predictions_df = pd.DataFrame (test_predictions, 
                                                columns = ['id', 
                                                           'estimatedEndDate'])

            validation_predictions_df.to_csv (self.prediction_file_path.replace ('.csv', '_validation.csv'), index = False)
            
            test_predictions_df.to_csv (self.prediction_file_path.replace ('.csv', '_test.csv'), index = False)
            
            print (f"\n Predictions saved successfully to {self.prediction_file_path}")
            
            # database = DataBase (dbname = 'your_db_name', 
            #                      user = 'your_user', 
            #                      password = 'your_password')
        
            # database.connect ()

            # database.insert_predictions (validation_predictions_df ['Prediction'].values, 
            #                              table_name = 'predictions')

            # database.close()
            
            print (f"\n Predictions saved successfully to {self.prediction_file_path}")
        
        except Exception as exception :
            
            print (f"\n Error saving predictions : \n {str (exception)}")
        
    """
    Fonction qui trace la performance du modele en fonction de la performance de validation et de test
    """
    def plot_performance (self) :
        
        mean_absolute_error_value = [value [1] for value in self.validation_performance.values ()]
        mean_absolute_error_test = [value [1] for value in self.performance.values ()]

        x = np.arange (len (self.performance))

        fig, axe = plt.subplots ()
        
        axe.bar (x - 0.15, 
                 mean_absolute_error_value, 
                 width = 0.25, 
                 color = 'black', 
                 edgecolor = 'black', 
                 label = 'Validation')
        
        axe.bar (x + 0.15, 
                 mean_absolute_error_test, 
                 width = 0.25, 
                 color = 'white', 
                 edgecolor = 'black', 
                 hatch = '/', 
                 label = 'Test')
        
        axe.set_ylabel ('Mean absolute error')
        axe.set_xlabel ('Models')

        for index, value in enumerate (mean_absolute_error_value) :
            
            plt.text (x = index - 0.15, 
                      y = value + 0.005, 
                      s = str (round (value, 3)), 
                      horizontalalignment = 'center')

        for index, value in enumerate (mean_absolute_error_test) :
            
            plt.text (x = index + 0.15, 
                      y = value + 0.0025, 
                      s = str (round (value, 3)), 
                      horizontalalignment = 'center')

        plt.ylim (0, 0.33)
        plt.xticks (ticks = x, 
                    labels = self.performance.keys ())
        plt.legend (loc = 'best')
        plt.tight_layout ()

        plt.savefig ('../figures/Global_results.png', 
                     dpi = 300)

    """
    Fonction qui execute les fonctions definie precedemment
    """
    def run (self) : 
    
        try : 
        
            if (not os.path.exists (self.train_file_path)) :    
        
                self.dataPreprocessor ()
            
            self.create_print_data_window ()
                        
            # self.dense_model ()
            self.lstm_model ()
            # self.cnn_lstm_model ()
            # self.arima_lstm_model ()
            
            self.plot_performance ()

        except Exception as exception :
            
            print (f"\n Error occurred during the run : \n {str (exception)} \n")

"""
Fonction qui execute le programme
"""
if (__name__ == "__main__") :
    
    main = Main (batch_size = 32)
    
    main.run ()
