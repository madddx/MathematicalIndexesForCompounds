from concurrent.futures import ThreadPoolExecutor
import requests
import pandas as pd
import pubchempy as pcp


def fetch_compound(name):
        compounds = pcp.get_compounds(name, "name")

        if not compounds:
            return None

        c = compounds[0]
        cid = c.cid

        # descriptors from PubChemPy
        smiles = c.canonical_smiles
        logp = c.xlogp
        psa = c.tpsa
        molar_ref = c.molecular_refractivity
        polarizability = c.polarizability
        molar_volume = c.molar_volume

        # experimental physical properties (PUG-View)
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
        r = requests.get(url)
        view = r.json()

        density = boiling = enthalpy = flash = surface = None

        for sec in view["Record"]["Section"]:
            if sec["TOCHeading"] == "Chemical and Physical Properties":
                for s in sec.get("Section", []):
                    for ss in s.get("Section", []):
                        title = ss.get("TOCHeading")

                        try:
                            val = ss["Information"][0]["Value"]["StringWithMarkup"][0]["String"]
                        except:
                            continue

                        if title == "Density":
                            density = val
                        elif title == "Boiling Point":
                            boiling = val
                        elif title == "Enthalpy of Vaporization":
                            enthalpy = val
                        elif title == "Flash Point":
                            flash = val
                        elif title == "Surface Tension":
                            surface = val

        return {
            "name": name,
            "smiles": smiles,
            "density": density,
            "boiling_point": boiling,
            "enthalpy": enthalpy,
            "flash_point": flash,
            "molar_refractivity": molar_ref,
            "logP": logp,
            "PSA": psa,
            "polarizability": polarizability,
            "surface_tension": surface,
            "molar_volume": molar_volume,
        }


def save_smiles():
    compound_names = (
        pd.read_csv("drug-bank.csv")["name"]
        .dropna()
        .drop_duplicates()[:501]
    )

    results = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        for res in executor.map(fetch_compound, compound_names):
            if res:
                print(f"✔ {res['name']}")
                results.append(res)
            else:
                print("Lookup Failed...")

    df = pd.DataFrame(results).drop_duplicates()
    df.to_csv("drug_properties.csv", index=False)