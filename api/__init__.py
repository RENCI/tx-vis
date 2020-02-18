import pdsphenotypemapping.dispatcher
import os

def mappingClinicalFromData(patient_id, timestamp, body):
    return pdsphenotypemapping.dispatcher.lookupClinicalsFromData(patient_id, timestamp, body)

config = {
    "title": "DOAC variable mapper",
    "pluginType": "m",
    "pluginTypeTitle": "Mapping",
    "pluginSelectors": [],
    "supportedPatientVariables": [
        {
            "id": i,
            "title": t,
            "legalValues": lv
        } for i,t,lv in [
            ("LOINC:2160-0", "Serum creatinine", {"type": "number"}),
            ("LOINC:82810-3", "Pregnancy", {"type": "boolean"}),
            ("HP:0001892", "Bleeding", {"type": "boolean"}),
            ("HP:0000077", "Kidney dysfunction", {"type": "boolean"}),
            ("LOINC:30525-0", "Age", {"type": "integer"}),
            ("LOINC:54134-2", "Race", {"type": "string"}),
            ("LOINC:54120-1", "Ethnicity", {"type": "string"}),
            ("LOINC:21840-4", "Sex", {"type": "string"}),
            ("LOINC:8302-2", "Height", {"type": "number"}),
            ("LOINC:29463-7", "Weight", {"type": "number"}),
            ("LOINC:39156-5", "BMI", {"type": "number"})
        ]
    ]
}

def get_config():
    return config

