from .utils import tstostr, strtots, unbundle, strtodate
from datetime import datetime, date
import os
import requests
import re
from oslash import Left, Right
from tx.utils import get, post

pds_host = os.environ["PDS_HOST"]
pds_port = os.environ["PDS_PORT"]


def pdsdpi_url_base(plugin):
    return f"https://{pds_host}:{pds_port}/v1/plugin/{plugin}"


def query_records(records, codes, timestamp):
    if records == None:
        return {
            "value": None,
            "certitude": 0,
            "calculation": "no record found"
        }

    def calculation(codes):
        return "from " + ",".join(list(map(lambda a: a["system"] + " " + a["code"], codes)))

    def extract_key(a):
        if "effectiveInstant" in a:
            return a["effectiveInstant"]
        if "onsetDateTime" in a:
            return a["onsetDateTime"]
        return None
    
    records_filtered = []
    for record in records:
        for c in codes:  
            system = c["system"]
            code = c["code"]
            is_regex = c["is_regex"]
            
            for c2 in record["code"]["coding"]: 
                if c2["system"] == system:
                    if (is_regex and re.search(code, "^" + c2["code"] + "$")) or c2["code"] == code:
                        records_filtered.append(record)
    if len(records_filtered) == 0:
        return {
            "value": None,
            "certitude": 0,
            "calculation": calculation(codes) 
        }
    else:
        ts = strtots(timestamp)
        def key(a):
            ext_key = extract_key(a)
            if ext_key is None:
                return float("inf")
            else:
                return abs(strtots(ext_key) - ts)
        record = min(records_filtered, key = key)
        keyr = extract_key(record)
        c = calculation(record["code"]["coding"])
        if keyr is None:
            c += " at notimestamp"
            cert = 1
        else:
            c += " at " + extract_key(record)
            cert = 2
        if "valueQuantity" in record:
            v = record["valueQuantity"]
        else:
            v = []
        return {
            "value": v,
            "certitude": cert,
            "calculation": c
        }
    

def get_observation(patient_id, plugin):
    resp = get(pdsdpi_url_base(plugin) + f"/Observation?patient={patient_id}", verify=False)
    return resp.map(lambda x : unbundle(x))


def get_condition(patient_id, plugin):
    resp = get(pdsdpi_url_base(plugin) + f"/Condition?patient={patient_id}", verify=False)
    return resp.map(lambda x : unbundle(x))


def get_patient(patient_id, plugin):
    resp = get(pdsdpi_url_base(plugin) + f"/Patient/{patient_id}", verify=False)
    if isinstance(resp, Left) and isinstance(resp.value[0], dict) and resp.value[0].get("status_code") == 404:
        return Right(None)
    else:
        return resp


def height(patient_id, timestamp, plugin):
    mrecords = get_observation(patient_id, plugin)
    return mrecords.map(lambda records: query_records(records, [
	    {
	        "system":"http://loinc.org",
	        "code":"8302-2",
	        "is_regex": False
	    }
        ], timestamp))


def weight(patient_id, timestamp, plugin):
    mrecords = get_observation(patient_id, plugin)
    return mrecords.map(lambda records: query_records(records, [
	    {
	        "system":"http://loinc.org",
	        "code":"29463-7",
	        "is_regex": False
	    }
        ], timestamp))


def bmi(patient_id, timestamp, plugin):
    mrecords = get_observation(patient_id, plugin)
    return mrecords.map(lambda records: query_records(records, [
	    {
	        "system":"http://loinc.org",
	        "code":"39156-5",
	        "is_regex": False
	    }
        ], timestamp))
    

def calculate_age2(born, timestamp):
    today = strtodate(timestamp)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def age(patient_id, timestamp, plugin):
    mpatient = get_patient(patient_id, plugin)
    def calculate_age(patient):
        if patient == None:
            return {
                "value": None,
                "certitude": 0,
                "calculation": "record not found"            
            }
        else:
            if "birthDate" in patient:
                birth_date = patient["birthDate"]
                date_of_birth = datetime.strptime(birth_date, "%Y-%m-%d")
                age = calculate_age2(date_of_birth, timestamp)
                return {
                    "value": age,
                    "certitude": 2,
                    "calculation": "birthDate"
                }
            else:
                return {
                    "value": None,
                    "certitude": 0,
                    "calculation": "birthDate not set"
                }
    return mpatient.map(calculate_age)


def sex(patient_id, timestamp, plugin):
    mpatient = get_patient(patient_id, plugin)
    def calculate_sex(patient):
        if patient == None:
            return {
                "value": None,
                "certitude": 0,
                "calculation": "record not found"            
            }
        else:
            return {
                "value": patient["gender"],
                "certitude": 2,
                "calculation": "gender"
            }
    return mpatient.map(calculate_sex)


def demographic_extension(url):
    def func(patient_id, timestamp, plugin):
        mpatient = get_patient(patient_id, plugin)
        def calculate_demographic(patient):
            if patient == None:
                return {
                    "value": None,
                    "certitude": 0,
                    "calculation": "record not found"            
                }
            else:
                extension = patient.get("extension")
                if extension is None:
                    return {
                        "value": None,
                        "certitude": 0,
                        "calculation": "extension not found"
                    }
                else:
                
                    filtered = filter(lambda x: x["url"]==url, extension)
                    if len(filtered) == 0:
                        return {
                            "value": None,
                            "certitude": 0,
                            "calculation": "extension not found"
                        }
                    else:
                        certitude = 2
                        value = []
                        calculation = url
                        hasValueCodeableConcept = True

                        for a in filtered:
                            valueCodeableConcept = a.get("valueCodeableConcept")
                            if valueCodeableConcept is None:
                                certitude = 1
                                calculation += " valueCodeableConcept not found"
                            else:
                                hasValueCodeableConcept = True
                                value.append(valueCodeableConcept)

                        if len(value) == 0:
                            certitude = 0
                        elif not hasValueCodeableConcept:
                            calculation += " on some extension"

                        return {
                            "value": value,
                            "certitude": certitude,
                            "calculation": calculation
                        }
        return mpatient.map(calculate_demographic)
    return func


race = demographic_extension("http://hl7.org/fhir/StructureDefinition/us-core-race")


ethnicity = demographic_extension("http://hl7.org/fhir/StructureDefinition/us-core-ethnicity")


def serum_creatinine(patient_id, timestamp, plugin):
    mrecords = get_observation(patient_id, plugin)
    return mrecords.map(lambda records: query_records(records, [
	{
	    "system":"http://loinc.org",
	    "code":"2160-0",
	    "is_regex": False
	}
    ], timestamp))


def pregnancy(patient_id, timestamp, plugin):
    mrecords = get_condition(patient_id, plugin)
    return mrecords.map(lambda records: query_records(records, [
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Z34\\.",
            "is_regex": True
        }
    ], timestamp))


def bleeding(patient_id, timestamp, plugin):
    mrecords = get_condition(patient_id, plugin)
    return mrecords.map(lambda records: query_records(records, [
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I60\\..*",
            "is_regex":True 
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I61\\..*",
            "is_regex":True
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I62\\..*",
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
            "code":"R58\\..*",
            "is_regex":True,
        }
    ], timestamp))


def kidney_dysfunction(patient_id, timestamp, plugin):
    mrecords = get_condition(patient_id, plugin)
    return mrecords.map(lambda records: query_records(records, [
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N00\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N10\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N17\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N14\\..*",
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
            "code":"I12\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I13\\..*",
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
            "code":"N01\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N02\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N03\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N04\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N05\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N06\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N07\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N08\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N11\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N13\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N15\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N16\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N18\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N19\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N25\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N26\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N27\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N28\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N29\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"Q60\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"Q61\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"Q62\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"Q63\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"Z49\\..*",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"Z99.2",
            "is_regex":True,
	    
        },
        {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N12\\..*",
            "is_regex":True,
	    
        }
    ], timestamp))


mapping = {
    "2160-0": serum_creatinine, # serum creatinine
    "82810-3": pregnancy, # pregnancy
    "HP:0001892": bleeding, # bleeding
    "HP:0000077": kidney_dysfunction, # kidney dysfunction
    "30525-0": age,
    "54134-2": race,
    "54120-1": ethnicity,
    "21840-4": sex,
    "8302-2": height,
    "29463-7": weight,
    "39156-5": bmi
}
