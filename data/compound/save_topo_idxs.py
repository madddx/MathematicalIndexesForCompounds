from rdkit import Chem
import pandas as pd
from topology import compute_topological_indices


def save_topo_idxs():
    smiles_df = pd.read_csv("phys_chem_properties.csv", index_col="name").dropna()

    indices_cols = [
        "M1", "M2", "HM", "H", "mm2", "ReZG3",
        "F", "IS", "A", "R", "RR", "ABC", "SC"
    ]

    indices = []

    n = len(smiles_df)

    for i, (idx, row) in enumerate(smiles_df.iterrows(), start=1):
        mol = Chem.MolFromSmiles(row["smiles"])

        ids_and_elements = {atom.GetIdx(): atom for atom in mol.GetAtoms()}

        indices.append(compute_topological_indices(ids_and_elements))

        print(f"{i} / {n}")

    # dataframe of computed indices
    indices_df = pd.DataFrame(indices, columns=indices_cols, index=smiles_df.index)

    # horizontal stack
    final_df = pd.concat([smiles_df, indices_df], axis=1)

    final_df.to_csv("data.csv")


if __name__ == "__main__":
    save_topo_idxs()