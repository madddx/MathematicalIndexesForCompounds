import pandas as pd
import numpy as np
import torch

data = pd.read_csv('data.csv')
data = data.drop(columns=['name', 'smiles', 'logP'])

# X: pd.DataFrame = data[['M1', 'M2', 'HM', 'H', 'mm2', 'ReZG3', 'F', 'IS', 'A', 'R', 'RR', 'ABC', 'SC']]
X: pd.DataFrame = data[['M1', 'HM', 'ReZG3', 'IS', 'SC', 'A']]
# Y: pd.DataFrame = data[['molecular_weight', 'melting_point_K', 'boiling_point_K', 'heat_of_fusion', 'heat_of_vaporization', 'critical_temperature', 'critical_pressure', 'flash_point']]
Y: pd.DataFrame = data[['melting_point_K', 'boiling_point_K']]

def apply_precision(df, precision_list):
    """
    Rounds each column of df according to precision_list.

    Args:
        df (pd.DataFrame): Input dataframe
        precision_list (list of float): Precision for each column

    Returns:
        pd.DataFrame: Rounded dataframe
    """
    if df.shape[1] != len(precision_list):
        raise ValueError("Number of columns must match length of precision_list")

    df = df.copy()

    for i, precision in enumerate(precision_list):
        col = df.columns[i]
        if precision <= 0:
            continue  # skip invalid precision
        
        df[col] = np.round(df[col] / precision) * precision
        
    return df

# precisions = [0.01, 0.1, 0.1, 0.01, 0.01, 0.1, 0.01, 0.1]
precisions = [0.1, 0.1]
Y = apply_precision(Y, precisions)

X = torch.from_numpy(X.to_numpy().astype(np.float32))
Y = torch.from_numpy(Y.to_numpy().astype(np.float32))

class CompoundDataset(torch.utils.data.Dataset):
    def __init__(self, X: torch.tensor, Y: torch.tensor):
        super().__init__()
        self.X = X
        self.Y = Y
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, index):
        return self.X[index], self.Y[index]

cd = CompoundDataset(X, Y)
torch.save(cd, "dataset.pt")