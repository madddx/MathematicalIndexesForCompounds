import torch
import imoltance
import numpy as np
import pandas as pd
from rdkit import Chem
from imoltance import Imoltance
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

import json
import random

smiles_col = 'SMILES'
target_cols = ['Tm']
data_path = 'bradley_open.csv'

def alt_get_bond_key(mol: Chem.rdchem.Mol, atom1: Chem.rdchem.Atom, atom2: Chem.rdchem.Atom):
    edge_names = tuple(sorted([atom1.GetSymbol(), atom2.GetSymbol()]))
    
    return f'{edge_names[0]}-{edge_names[1]}'

def alt_get_element_key(atom: Chem.rdchem.Atom):
    return f'{atom.GetSymbol()}'

def record(name: str, train_path: str, test_path: str, seed: int):
    train_data_df = pd.read_csv(train_path)
    test_data_df = pd.read_csv(test_path)
    
    X_train = train_data_df[[
                            'M1_alpha_ve', 'M1_beta_ve', 'M2_ve', 'R_ve', 'ABC_ve', 'GA_ve',
                            'H_ve', 'X_ve', 'HM1_ve', 'HM2_ve', 'F_ve', 'F1_ve',
                            'ReZG3_ve', 'AG_ve', 'ISI_ve', 'T_ve', 'ID_ve', 'ZD_ve',
                            'mM1_ve', 'T_ev', 'M_ev', 'F_ev', 'mM_ev', 'ID_ev',
                            'R_ev', 'RR_ev'
                        ]]
    Y_train = train_data_df[target_cols]


    X_test = test_data_df[[
                            'M1_alpha_ve', 'M1_beta_ve', 'M2_ve', 'R_ve', 'ABC_ve', 'GA_ve',
                            'H_ve', 'X_ve', 'HM1_ve', 'HM2_ve', 'F_ve', 'F1_ve',
                            'ReZG3_ve', 'AG_ve', 'ISI_ve', 'T_ve', 'ID_ve', 'ZD_ve',
                            'mM1_ve', 'T_ev', 'M_ev', 'F_ev', 'mM_ev', 'ID_ev',
                            'R_ev', 'RR_ev'
                        ]]
    Y_test = test_data_df[target_cols]

    x_scaler = StandardScaler()
    X_train = x_scaler.fit_transform(X_train)
    X_test = x_scaler.transform(X_test)
    
    model = RandomForestRegressor(
        n_estimators=500,
        max_features=0.33,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        bootstrap=True,
        oob_score=True,
        random_state=seed,
        n_jobs=-1,
    )
    
    model.fit(X_train, Y_train)
    
    predictions = model.predict(X_test)
    r2 = r2_score(Y_test, predictions)
    mse = mean_squared_error(Y_test, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(Y_test, predictions)

    print("R²:", r2)
    print("MSE:", mse)
    print("RMSE:", rmse)
    print("MAE:", mae)
    
    data = {
        'name': name,
        'seed': seed,
        'r2': r2,
        'mse': mse,
        'rmse': rmse,
        'mae': mae
    }
    
    return data

def run(seed):

    # Python
    random.seed(seed)
    # NumPy
    np.random.seed(seed)
    
    imlt = Imoltance(data_path, smiles_col, target_cols, seed)
    
    imlt.run_basic()
    data_basic = record('no stereo + no learned weights', 'imoltance_dump/train_features_basic.csv', 'imoltance_dump/test_features_basic.csv', seed)
    
    imoltance.config.get_bond_key = alt_get_bond_key
    imoltance.config.get_element_key = alt_get_element_key
    imlt.run()
    data_nslw = record('no stereo + learned weights', 'imoltance_dump/train_features.csv', 'imoltance_dump/test_features.csv', seed)
    
    imoltance.config.get_bond_key = imoltance.config.default_get_bond_key
    imoltance.config.get_element_key = imoltance.config.default_get_element_key
    imlt.run()
    data_slw = record('stereo + learned weights', 'imoltance_dump/train_features.csv', 'imoltance_dump/test_features.csv', seed)
    
    with open(f'{seed}.json', 'w') as file:
        json.dump([data_basic, data_nslw, data_slw], file)
    
        
run(321)
run(125)
run(3)
run(56)
run(74)
run(1)