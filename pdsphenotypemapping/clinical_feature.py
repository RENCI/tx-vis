from .utils import tstostr, strtots, unbundle, strtodate
from datetime import datetime, date
import os
import requests


pdsdpi_host = os.environ["PDSDPI_HOST"]
pdsdpi_port = os.environ["PDSDPI_PORT"]


pdsdpi_url_base = f"http://{pdsdpi_host}:{pdsdpi_port}"


def query_records(records, codes, timestamp):
    def calculation(codes):
        return "from " + ",".join(list(map(lambda a: a["system"] + " " + a["code"], codes)))
    records_filtered = []
    for record in records:
        for c in codes:  
            system = c["system"]
            code = c["code"]
            certitude = c["certitude"]
            
            for c2 in resc["code"]["coding"]: 
                if c2["system"] == system:
                    if (is_regex and re.search(code, "^" + c2["code"] + "$")) or c2["code"] == code:
                        records_filtered.append(resc)
    if len(records_filtered == 0):
        return {
            "value": "unset",
            "certitude": 0,
            "calculation": calculation(codes) 
        }
    else:
        ts = strtots(timestamp)
        record = min(records_filtered, key = lambda a: abs(strtots(a["effectiveInstant"]) - ts))
        return {
            "value": record["valueQuantity"],
            "certitude": 2,
            "calculation": calculation(record["code"]["coding"]) + " at " + record["effectiveInstant"]
        }
    

def get_observation(patient_id):
    resp = requests.get(f"{pdsdpi_url_base}/Observation?patient={patient_id}")
    if resp.status_code == 200:
        return unbundle(resp.json())
    else:
        return None


def get_condition(patient_id):
    resp = requests.get(f"{pdsdpi_url_base}/Condition?patient={patient_id}")
    if resp.status_code == 200:
        return unbundle(resp.json())
    else:
        return None


def get_patient(patient_id):
    resp = requests.get(f"{pdsdpi_url_base}/Patient/{patient_id}")
    if resp.status_code == 200:
        return resp.json()
    else:
        return None


def height(patient_id, timestamp):
    records = get_observation(patient_id)
    if records == None:
        return {
            "value": null,
            "certitude": 0,
            "calculation": "record not found"            
        }
    else:
        return query_records(records, [
	    {
	        "system":"http://loinc.org",
	        "code":"8302-2",
	        "is_regex": False
	    }
        ], timestamp)


def weight(patient_id, timestamp):
    records = get_observation(patient_id)
    if records == None:
        return {
            "value": null,
            "certitude": 0,
            "calculation": "record not found"            
        }
    else:
        return query_records(records, [
	    {
	        "system":"http://loinc.org",
	        "code":"29463-7",
	        "is_regex": False
	    }
        ], timestamp)


def bmi(patient_id, timestamp):
    records = get_observation(patient_id)
    if records == None:
        return {
            "value": null,
            "certitude": 0,
            "calculation": "record not found"            
        }
    else:
        return query_records(records, [
	    {
	        "system":"http://loinc.org",
	        "code":"39156-5",
	        "is_regex": False
	    }
        ], timestamp)
    

def calculate_age(born, timestamp):
    today = strtodate(timestamp)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def age(patient_id, timestamp):
    patient = get_patient(patient_id)
    if patient == None:
        return {
            "value": null,
            "certitude": 0,
            "calculation": "record not found"            
        }
    else:
        if "birthDate" in patient:
            birth_date = patient["birthDate"]
            date_of_birth = datetime.strptime(birth_date, "%Y-%m-%d")
            age = calculate_age(date_of_birth, timestamp)
            return {
                "value": age,
                "certitude": 2,
                "calculation": "birthDate"
            }
        else:
            return {
                "value": null,
                "certitude": 0,
                "calculation": "birthDate not set"
            }


def gender(patient_id, timestamp):
    patient = get_patient(patient_id)
    if patient == None:
        return {
            "value": null,
            "certitude": 0,
            "calculation": "record not found"            
        }
    else:
        return {
            "value": patient["gender"],
            "certitude": 2,
            "calculation": "gender"
        }


def race(patient_id, timestamp):
    patient = get_patient(patient_id)
    if patient == None:
        return {
            "value": null,
            "certitude": 0,
            "calculation": "record not found"            
        }
    else:
        return {
            "value": list(map(lambda a: a["valueCodeableConcept"],filter(lambda x: x["url"]=="http://hl7.org/fhir/StructureDefinition/us-core-race",patient["extension"]))),
            "certitude": 2,
            "calculation": "http://hl7.org/fhir/StructureDefinition/us-core-race"
        }


def ethnicity(patient_id, timestamp):
    patient = get_patient(patient_id)
    if patient == None:
        return {
            "value": null,
            "certitude": 0,
            "calculation": "record not found"            
        }
    else:
        return {
            "value": list(map(lambda a: a["valueCodeableConcept"],filter(lambda x: x["url"]=="http://hl7.org/fhir/StructureDefinition/us-core-ethnicity",patient["extension"]))),
            "certitude": 2,
            "calculation": "http://hl7.org/fhir/StructureDefinition/us-core-ethnicity"
        }


def serum_creatinine(patient_id, timestamp):
    return query_records(get_observation(patient_id), [
	{
	    "system":"http://loinc.org",
	    "code":"2160-0",
	    "is_regex": False
	}
    ], timestamp)


def pregnancy(patient_id, timestamp):
    return query_records(get_condition(patient_id), [
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Z34\\.",
            "is_regex": True
        }
    ], timestamp)


def bleeding(patient_id, timestamp):
    return query_records(get_condition(patient_id), [
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^I60\\.",
            "is_regex":True 
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^I61\\.",
            "is_regex":True
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^I62\\.",
            "is_regex":True
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"G95.19",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"T85.830",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H11.3",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H31.3",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H43.1",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H59.1",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H59.3",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I85.01",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K22.11",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H22.6",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H25.0",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H25.2",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H25.4",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H25.6",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H26.0",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H26.2",
            "is_regex":False
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H26.4",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H26.6",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H27.0",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H27.2",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H27.4",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H27.6",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H28.0",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H28.2",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H28.4",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H28.6",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K29.01",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K31.811",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K92.0",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K55.21",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.01",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.21",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.31",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.33",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.41",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.51",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.53",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.81",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.91",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.93",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K62.5",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K92.1",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K92.2",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K66.1",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"M25.0",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I31.2",
            "is_regex":False,
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^R58\\.",
            "is_regex":True,
        }
    ], timestamp)


def kidney_dysfunction(patient_id, timestamp):
    query_records(get_condition(patient_id), [
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N00\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N10\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N17\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N14\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N14.1",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N14.2",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"T36.5X5",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"B52.0",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"D59.3",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"E10.2",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"E11.2",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"E13.2",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^I12\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^I13\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I15.1",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I15.2",
            "is_regex":False,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N01\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N02\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N03\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N04\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N05\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N06\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N07\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N08\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N11\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N13\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N15\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N16\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N18\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N19\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N25\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N26\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N27\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N28\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N29\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Q60\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Q61\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Q62\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Q63\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Z49\\.",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"Z99.2",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N12\\.",
            "is_regex":True,
	    
        }
    ], timestamp)


mapping = {
    "2160-0": serum_creatinine, # serum creatinine
    "82810-3": pregnancy, # pregnancy
    "HP:0001892": bleeding, # bleeding
    "HP:0000077": kidney_dysfunction, # kidney dysfunction
    "age": age,
    "race": race,
    "ethnicity": ethnicity,
    "gender": gender,
    "8302-2": height,
    "29463-7": weight,
    "39156-5": bmi
}
