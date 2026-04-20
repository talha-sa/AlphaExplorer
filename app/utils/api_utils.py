# AlphaExplorer - API Utilities
# Handles all external API calls

import requests
import pandas as pd

# ── AlphaFold API ─────────────────────────────────────────────

def get_alphafold_structure(uniprot_id):
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if data:
                return data[0]
    except Exception as e:
        print(f"AlphaFold error: {e}")
    return None

def get_pdb_string(pdb_url):
    try:
        r = requests.get(pdb_url, timeout=15)
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"PDB fetch error: {e}")
    return None

# ── UniProt API ───────────────────────────────────────────────

def search_uniprot(query, limit=5):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"{query} AND reviewed:true",
        "format": "json",
        "size": limit,
        "fields": "accession,protein_name,gene_names,organism_name,length,function,disease,go"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            return data.get("results", [])
    except Exception as e:
        print(f"UniProt search error: {e}")
    return []

def get_uniprot_details(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}"
    params = {"format": "json"}
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"UniProt details error: {e}")
    return None

def extract_protein_info(uniprot_data):
    if not uniprot_data:
        return {}

    info = {}

    # Protein name
    try:
        info["name"] = uniprot_data["proteinDescription"][
            "recommendedName"]["fullName"]["value"]
    except:
        info["name"] = "Unknown"

    # Gene name
    try:
        info["gene"] = uniprot_data["genes"][0][
            "geneName"]["value"]
    except:
        info["gene"] = "Unknown"

    # Organism
    try:
        info["organism"] = uniprot_data["organism"][
            "scientificName"]
    except:
        info["organism"] = "Unknown"

    # Length
    try:
        info["length"] = uniprot_data["sequence"]["length"]
    except:
        info["length"] = "Unknown"

    # Function
    try:
        comments = uniprot_data.get("comments", [])
        for c in comments:
            if c.get("commentType") == "FUNCTION":
                info["function"] = c["texts"][0]["value"]
                break
    except:
        info["function"] = "Not available"

    # Diseases
    try:
        diseases = []
        for c in uniprot_data.get("comments", []):
            if c.get("commentType") == "DISEASE":
                try:
                    diseases.append(c["disease"]["diseaseId"])
                except:
                    pass
        info["diseases"] = diseases
    except:
        info["diseases"] = []

    # Subcellular location
    try:
        for c in uniprot_data.get("comments", []):
            if c.get("commentType") == "SUBCELLULAR LOCATION":
                locs = c.get("subcellularLocations", [])
                info["location"] = ", ".join([
                    l["location"]["value"] for l in locs
                ])
                break
    except:
        info["location"] = "Unknown"

    return info

# ── ChEMBL API ────────────────────────────────────────────────

def get_chembl_drugs(uniprot_id, limit=10):
    # First find the ChEMBL target ID
    target_url = "https://www.ebi.ac.uk/chembl/api/data/target"
    params = {
        "target_components__accession": uniprot_id,
        "format": "json",
        "limit": 5
    }
    try:
        r = requests.get(target_url, params=params, timeout=15)
        if r.status_code != 200:
            return []

        targets = r.json().get("targets", [])
        if not targets:
            return []

        chembl_id = targets[0]["target_chembl_id"]

        # Now fetch approved drugs
        drug_url = "https://www.ebi.ac.uk/chembl/api/data/drug_indication"
        drug_params = {
            "target_chembl_id": chembl_id,
            "format": "json",
            "limit": limit
        }
        dr = requests.get(drug_url, params=drug_params, timeout=15)
        if dr.status_code == 200:
            return dr.json().get("drug_indications", [])

    except Exception as e:
        print(f"ChEMBL error: {e}")
    return []

def get_similar_proteins(uniprot_id, limit=5):
    url = f"https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"sequence_checksum:{uniprot_id} AND reviewed:true",
        "format": "json",
        "size": limit
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("results", [])
    except:
        pass
    return []