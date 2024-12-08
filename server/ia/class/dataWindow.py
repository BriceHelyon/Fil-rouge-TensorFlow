import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 7.5)
plt.rcParams['axes.grid'] = False

tf.random.set_seed (42)
np.random.seed (42)

"""
Classe DataWindow pour la creation des fenetres de donnees
"""
class DataWindow () :
    
    """
    Constructeur de la classe DataWindow
    """    
    def __init__(self, 
                 input_width, 
                 label_width, 
                 shift, 
                 train_dataframe,
                 label_columns = None,
                 batch_size = 32) :
        
        self.train_dataframe = train_dataframe
        self.label_columns = label_columns
        self.batch_size = batch_size
        
        if (label_columns is not None) :
        
            self.label_columns_indices = {
                name: i for i, name in enumerate (label_columns)
                }
        
        self.column_indices = {
            name: i for i, name in enumerate (train_dataframe.columns)
            }
        
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
        
        self.total_window_size = input_width + shift
        
        self.input_slice = slice (0, input_width)
        self.input_indices = np.arange (self.total_window_size) [self.input_slice]
        
        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice (self.label_start, None)
        self.label_indices = np.arange (self.total_window_size) [self.labels_slice]
    
    """
    Methode split_to_inputs_labels pour separer les donnees en entrees et sorties
    """
    def split_to_inputs_labels (self, 
                                features) :
        
        inputs = features [:, self.input_slice, :]
        labels = features [:, self.labels_slice, :]
        
        print(f"\n Inputs shape after split: {inputs.shape}")
        print(f"Labels shape after split: {labels.shape}")
        
        if (self.label_columns is not None) :
        
            missing_columns = [name for name in self.label_columns 
                               if (name not in self.column_indices)]
        
            if (missing_columns) :
            
                raise KeyError (f"Label columns missing from dataframe : \n {missing_columns}")
        
            labels = tf.stack(
                [labels [:, :, self.column_indices [name]] for name in self.label_columns],
                axis = - 1
            )
        
        inputs.set_shape ([None, self.input_width, None])
        labels.set_shape ([None, self.label_width, None])
        
        print (f"\n Inputs shape after setting shape : {inputs.shape}")
        print (f"Labels shape after setting shape : {labels.shape}")
        
        return inputs, labels
    
    """
    Methode plot pour visualiser les donnees
    """
    def plot (self, 
              model = None, 
              plot_column = 'life', 
              max_subplots = 3) :
        
        inputs, labels = self.sample_batch
        
        print (f"\n Inputs shape : {inputs.shape}")
        print (f"\n Labels shape : {labels.shape}")


        print (f"\n Input indices shape: {self.input_indices.shape}")
        print (f"\n Label indices shape: {self.label_indices.shape}")
        
        plt.figure (figsize = (12, 8))
        plot_column_index = self.column_indices [plot_column]
        maximum_number = min (max_subplots, len (inputs))
        
        for n in range (maximum_number):
            
            plt.subplot (3, 
                         1, 
                         n + 1)
            plt.ylabel (f'{plot_column} [scaled]')
            plt.plot (self.input_indices, 
                      inputs [n, :, plot_column_index],
                      label = 'Inputs', 
                      marker = '.', 
                      zorder = - 10)

            if (self.label_columns) :
    
                label_column_index = self.label_columns_indices.get (plot_column, 
                                                                     None)
            
            else:
    
                label_column_index = plot_column_index

            if (label_column_index is None) :
    
              continue

            plt.scatter (self.label_indices, 
                         labels [n, :, label_column_index],
                         edgecolors = 'k', 
                         marker = 's', 
                         label = 'Labels', 
                         c = 'green', 
                         s = 64)
    
            if (model is not None) :
    
              predictions = model (inputs)
    
              plt.scatter (self.label_indices, 
                           predictions [n, :, label_column_index],
                           marker = 'X', 
                           edgecolors = 'k', 
                           label = 'Predictions',
                           c = 'red', 
                           s = 64)

            if (n == 0) :
    
              plt.legend()

        plt.xlabel ('Time (h)')
    
    """
    Methode make_dataset pour creer le dataset
    """    
    def make_dataset (self, 
                      data) :
    
        data = np.array (data, 
                         dtype = np.float32)
        
        print (f"\n Data shape : {data.shape}")
    
        dataset = tf.keras.preprocessing.timeseries_dataset_from_array (
            data = data,
            targets = None,
            sequence_length = self.total_window_size,
            sequence_stride = 1,
            shuffle = True,
            batch_size = 32
        )
        
        for batch in dataset.take (1) :
        
            inputs, labels = self.split_to_inputs_labels (batch)
        
            print (f"\n Dataset batch inputs shape : {inputs.shape}")
            print (f"\n Dataset batch labels shape : {labels.shape}")
        
        dataset = dataset.map (self.split_to_inputs_labels)
    
        return dataset
    
    """
    Methode train pour recuperer les donnees d'entrainement
    """
    @property
    def train (self) :
        
        train_dataset = self.make_dataset (self.train_dataframe)
    
        return train_dataset
    
    """
    Methode validation pour recuperer les donnees de validation
    """
    @property
    def validation (self) :
        
        validation_dataset = self.make_dataset (self.train_dataframe)
    
        return validation_dataset
    
    """
    Methode test pour recuperer les donnees de test
    """
    @property
    def test (self) :
        
        test_dataset = self.make_dataset (self.train_dataframe)
    
        return test_dataset
    
    """
    Methode sample_batch pour recuperer un batch (echantillon)    
    """
    @property
    def sample_batch (self):
    
        result = getattr (self, 
                          '_sample_batch', 
                          None)
    
        if (result is None) :
    
            result = next (iter (self.test))
            
            self._sample_batch = result
    
        return result
    
    """
    Methode train_batches pour calculer le nombre de batchs (echantillons) d'entrainement
    """
    @property
    def train_batches (self) :
        
        train_batches = self.calculate_batches (len (self.train_dataframe), self.batch_size)
        
        return train_batches

    """
    Methode validation_batches pour calculer le nombre de batchs (echantillons) de validation
    """
    @property
    def validation_batches (self) :
        
        validation_batches = self.calculate_batches (len (self.train_dataframe), self.batch_size)
        
        return validation_batches

    """
    Methode test_batches pour calculer le nombre de batchs (echantillons) de test
    """
    @property
    def test_batches (self) :
        
        test_batches = self.calculate_batches (len (self.train_dataframe), self.batch_size)
        
        return test_batches
    
    """
    Methode calculate_batches pour calculer le nombre de batchs (echantillons)
    """
    def calculate_batches (self, 
                           dataframe_length, 
                           batch_size) :
        
        number_batches = dataframe_length // batch_size
        
        if (dataframe_length % batch_size != 0) :
            
            number_batches += 1
            
        return number_batches