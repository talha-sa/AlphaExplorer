# AlphaExplorer - API Utilities
# Robust version with full error handling

import requests

# ── AlphaFold API ─────────────────────────────────────────────

def get_alphafold_structure(uniprot_id):
    try:
        url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if data and len(data) > 0:
                return data[0], None
        return None, f"AlphaFold returned status {r.status_code}"
    except requests.exceptions.Timeout:
        return None, "AlphaFold API timed out. Try again."
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to AlphaFold. Check internet."
    except Exception as e:
        return None, f"AlphaFold error: {str(e)}"

def get_pdb_string(pdb_url):
    try:
        r = requests.get(pdb_url, timeout=20)
        if r.status_code == 200:
            return r.text, None
        return None, f"PDB fetch failed: {r.status_code}"
    except requests.exceptions.Timeout:
        return None, "PDB download timed out."
    except Exception as e:
        return None, f"PDB error: {str(e)}"

# ── UniProt API ───────────────────────────────────────────────

def search_uniprot(query, limit=8):
    try:
        url = "https://rest.uniprot.org/uniprotkb/search"
        params = {
            "query": query,
            "format": "json",
            "size": limit,
            "fields": (
                "accession,protein_name,gene_names,"
                "organism_name,length,cc_function,"
                "cc_disease,go,cc_subcellular_location"
            )
        }
        r = requests.get(
            url, params=params,
            headers={"Accept": "application/json"},
            timeout=20
        )
        if r.status_code == 200:
            results = r.json().get("results", [])
            return results, None
        return [], f"UniProt search failed: {r.status_code}"
    except requests.exceptions.Timeout:
        return [], "UniProt search timed out."
    except requests.exceptions.ConnectionError:
        return [], "Cannot connect to UniProt. Check internet."
    except Exception as e:
        return [], f"UniProt error: {str(e)}"

def get_uniprot_details(uniprot_id):
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}"
        r = requests.get(
            url,
            params={"format": "json"},
            headers={"Accept": "application/json"},
            timeout=20
        )
        if r.status_code == 200:
            return r.json(), None
        return None, f"UniProt fetch failed: {r.status_code}"
    except requests.exceptions.Timeout:
        return None, "UniProt timed out."
    except Exception as e:
        return None, f"UniProt error: {str(e)}"

def extract_protein_info(data):
    if not data:
        return {}
    info = {}

    # Name
    try:
        info["name"] = (
            data["proteinDescription"]
               ["recommendedName"]
               ["fullName"]["value"]
        )
    except:
        try:
            info["name"] = (
                data["proteinDescription"]
                   ["submittedNames"][0]
                   ["fullName"]["value"]
            )
        except:
            info["name"] = "Unknown protein"

    # Gene
    try:
        info["gene"] = data["genes"][0]["geneName"]["value"]
    except:
        info["gene"] = "N/A"

    # Organism
    try:
        info["organism"] = data["organism"]["scientificName"]
    except:
        info["organism"] = "Unknown"

    # Length
    try:
        info["length"] = data["sequence"]["length"]
    except:
        info["length"] = "N/A"

    # Function
    info["function"] = "Not available"
    try:
        for c in data.get("comments", []):
            if c.get("commentType") == "FUNCTION":
                info["function"] = c["texts"][0]["value"]
                break
    except:
        pass

    # Diseases
    info["diseases"] = []
    try:
        for c in data.get("comments", []):
            if c.get("commentType") == "DISEASE":
                try:
                    disease_id = c["disease"]["diseaseId"]
                    disease_name = c["disease"].get(
                        "diseaseName", {}).get("value", disease_id
                    )
                    info["diseases"].append(disease_name)
                except:
                    pass
    except:
        pass

    # Subcellular location
    info["location"] = "Unknown"
    try:
        for c in data.get("comments", []):
            if c.get("commentType") == "SUBCELLULAR LOCATION":
                locs = c.get("subcellularLocations", [])
                info["location"] = ", ".join([
                    l["location"]["value"]
                    for l in locs
                    if "location" in l
                ])
                break
    except:
        pass

    # GO Terms — scientifically accurate parsing
    # GO prefixes: P = Biological Process,
    #              F = Molecular Function,
    #              C = Cellular Component
    info["go_biological"]  = []
    info["go_molecular"]   = []
    info["go_cellular"]    = []
    try:
        for ref in data.get("dbReferences", []):
            if ref.get("type") == "GO":
                props = ref.get("properties", {})
                term  = props.get("term", "")
                # First character indicates category
                if term.startswith("P:"):
                    info["go_biological"].append(term[2:])
                elif term.startswith("F:"):
                    info["go_molecular"].append(term[2:])
                elif term.startswith("C:"):
                    info["go_cellular"].append(term[2:])
    except:
        pass

    return info

# ── ChEMBL API ────────────────────────────────────────────────

# Scientifically accurate phase labels
PHASE_LABELS = {
    4: "✅ Approved",
    3: "🔬 Phase 3",
    2: "🧪 Phase 2",
    1: "🔭 Phase 1",
    0: "💡 Preclinical",
    -1: "❌ Discontinued"
}

def get_chembl_drugs(uniprot_id, limit=20):
    try:
        # Step 1: Find ChEMBL target from UniProt accession
        target_url = (
            "https://www.ebi.ac.uk/chembl/api/data/target"
        )
        r = requests.get(
            target_url,
            params={
                "target_components__accession": uniprot_id,
                "format": "json",
                "limit": 5
            },
            timeout=15
        )
        if r.status_code != 200:
            return [], f"ChEMBL target lookup failed: {r.status_code}"

        targets = r.json().get("targets", [])
        if not targets:
            return [], "No ChEMBL target found for this protein."

        chembl_id = targets[0]["target_chembl_id"]

        # Step 2: Fetch drug indications for this target
        dr = requests.get(
            "https://www.ebi.ac.uk/chembl/api/data/drug_indication",
            params={
                "target_chembl_id": chembl_id,
                "format": "json",
                "limit": limit
            },
            timeout=15
        )
        if dr.status_code != 200:
            return [], f"ChEMBL drug fetch failed: {dr.status_code}"

        drugs = dr.json().get("drug_indications", [])

        # Step 3: Enrich with phase labels
        enriched = []
        for d in drugs:
            phase_num = d.get("max_phase_for_ind")
            try:
                phase_num = int(phase_num)
            except:
                phase_num = -1
            enriched.append({
                "Drug Name"   : d.get("molecule_name", "Unknown"),
                "ChEMBL ID"   : d.get("molecule_chembl_id", "N/A"),
                "Indication"  : d.get("efo_term", "N/A"),
                "Phase"       : PHASE_LABELS.get(phase_num, "Unknown"),
                "Phase Number": phase_num
            })

        # Sort by phase (approved first)
        enriched.sort(
            key=lambda x: x["Phase Number"],
            reverse=True
        )
        return enriched, None

    except requests.exceptions.Timeout:
        return [], "ChEMBL API timed out."
    except requests.exceptions.ConnectionError:
        return [], "Cannot connect to ChEMBL. Check internet."
    except Exception as e:
        return [], f"ChEMBL error: {str(e)}"