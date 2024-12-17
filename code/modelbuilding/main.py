import os
import math

from sklearn.preprocessing import MinMaxScaler
import pandas as pd


from models.adaptivetabnet import AdaptiveTabNet
from models.cfrecoensemble import CFREcoEnsemble
from models.deepgreendnn import DeepGreenDNN
from models.ecocnn import EcoCNN
from models.opticarbonet import OptiCarboNet

def load_data(path):
    files = os.listdir(path)
    files_int = [int(file.split(".")[0]) for file in files if file.endswith(".parquet")]
    files_int.sort()

    train_perc = math.floor(0.7*len(files_int))
    test_perc = math.ceil(0.15*len(files_int))
    val_perc = math.ceil(0.15*len(files_int))

    train = files_int[:train_perc]
    test = files_int[train_perc:train_perc+test_perc]
    val = files_int[train_perc+test_perc:train_perc+test_perc+val_perc]

    train_files = [str(file)+".parquet" for file in train]
    test_files = [str(file)+".parquet" for file in test]
    val_files = [str(file)+".parquet" for file in val]

    return train_files, test_files, val_files

def process_data(datapath, train, test, val):
    
    trains, tests, vals = [], [], []

    trains = [pd.read_parquet(f"{datapath}{file}") for file in train]
    tests = [pd.read_parquet(f"{datapath}{file}") for file in test]
    vals = [pd.read_parquet(f"{datapath}{file}") for file in val]

    train_df = pd.concat(trains)
    test_df = pd.concat(tests)
    val_df = pd.concat(vals)
    
    pre_X_train = train_df[['rh', 'Elevation', 'NonVegetated', 
                        'TreeCover', 'PFTClass', 'Cover', 
                        'PAI', 'LST', 'NDVI']]
    y_train = train_df['Carbon']

    pre_X_test = test_df[['rh', 'Elevation', 'NonVegetated', 
                        'TreeCover', 'PFTClass', 'Cover', 
                        'PAI', 'LST', 'NDVI']]
    y_test = test_df['Carbon']

    pre_X_val = val_df[['rh', 'Elevation', 'NonVegetated', 
                        'TreeCover', 'PFTClass', 'Cover', 
                        'PAI', 'LST', 'NDVI']]
    y_val = val_df['Carbon']

    # Preprocessing pipeline for numeric features
    numeric_transformer = MinMaxScaler()

    # Apply preprocessing
    X_train = numeric_transformer.fit_transform(pre_X_train)
    X_test = numeric_transformer.fit_transform(pre_X_test)
    X_val = numeric_transformer.fit_transform(pre_X_val)

    return X_train, X_val, X_test, y_train, y_val, y_test


if __name__=="__main__":

    # Load the data
    datapath = "../../Dataset/"
    train, test, val = load_data(datapath)
    
    # Load and preprocess data
    X_train, X_val, X_test, y_train, y_val, y_test = process_data(datapath, train, test, val)

    y_pred_ann = OptiCarboNet.build(X_train, X_test, X_val, y_train, y_test, y_val)
    y_pred_tab = AdaptiveTabNet.build(X_train, X_test, X_val, y_train, y_test, y_val)
    y_pred_cnn = EcoCNN.build(X_train, X_test, X_val, y_train, y_test, y_val)
    y_pred_hyb = CFREcoEnsemble.build(X_train, X_test, X_val, y_train, y_test, y_val)
    y_pred_dnn = DeepGreenDNN.build(X_train, X_test, X_val, y_train, y_test, y_val)



