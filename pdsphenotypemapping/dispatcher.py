import json
import os
import re
from clinical_feature import mapping

# Function for loading patient record file(s)

def loadFHIR(input_file):
    with open(input_file) as inp_file:
        return json.load(inp_file)

# Error-handling function in case of no records or multiple records for a patient
    
def patientNumber(records):
    if len(records)>1:
        raise RuntimeError("Multiple Patient Records")
    elif len(records)==0:
        raise RuntimeError("No Patient Records")
    return records[0]

# Function that returns patient's demographic and clinical feature data

def lookupClinical(input_dir, patient_id, clinical):
    if clinical=="birth date":
         records=lookupPatient(input_dir,patient_id)
         patient=patientNumber(records)
         return patient["birthDate"]
    if clinical=="gender":
        records=lookupPatient(input_dir,patient_id)
        patient=patientNumber(records)
        return patient["gender"]
    if clinical=="race":
        records=lookupPatient(input_dir,patient_id)
        patient=patientNumber(records)
        return list(map(lambda a: a["valueCodeableConcept"],filter(lambda x: x["url"]=="http://hl7.org/fhir/StructureDefinition/us-core-race",patient["extension"])))
    if clinical=="ethnicity":
        records=lookupPatient(input_dir,patient_id)
        patient=patientNumber(records)
        return list(map(lambda a: a["valueCodeableConcept"],filter(lambda x: x["url"]=="http://hl7.org/fhir/StructureDefinition/us-core-ethnicity",patient["extension"])))
    
    codes=mapping[clinical]
    records=lookupFHIR(input_dir, patient_id, codes)
    return records

def lookupPatient(input_dir,patient_id):
    records=[]
    for root,_,fnames in os.walk(input_dir,topdown=True):
        for f in fnames:
            resc= loadFHIR(os.path.join(root,f))
            if resc["resourceType"] == "Patient":
                if resc["id"]==patient_id:
                    records.append(resc)
    return records
            
def lookupFHIR(input_dir, patient_id, clinical_query): # 'codes' parameter is an object of the form {"codes":[{"system":"", "code":"","is_regex":"","certitude":""}],"unavailable":{"certitude":""}}
    codes=clinical_query["codes"]
    unavailable=clinical_query["unavailable"]
    records = []
    for root, _, fnames in os.walk(input_dir, topdown=True):
        for f in fnames:
            resc = loadFHIR(os.path.join(root,f))
            for c in codes:  
                system = c["system"]
                code = c["code"]
                certitude = c["certitude"]
                if system == "http://loinc.org":
                    resc_type = "Observation"
                    print ("Observation")
                elif system == "http://hl7.org/fhir/sid/icd-10":
                    resc_type = "Condition"
                    print ("Condition")
                elif system == "http://hl7.org/fhir/sid/icd-10-cm":
                    resc_type = "Condition"
                    print ("Condition")
                elif system == "http://hl7.org/fhir/sid/icd-9-cm":
                    resc_type = "Condition"
                    print ("Condition")
                else:
                    print ("Unknown resource type")

                pid = resc["subject"]["reference"].split("/")
                
                if resc["resourceType"] == resc_type:
                    print ("resource type matched")
                    
                    # compares patient_ids
                    
                    if patient_id == pid[1]:
                        print("patient found")

                        # compares system and diagnosis codes
                        
                        for c2 in resc["code"]["coding"]: 
                            if c2["system"] == system:
                                if is_regex:
                                    if re.search(code, c2["code"]):
                                        print ("System and diagnosis code matched")                        
                                        records.append({"record":resc,"certitude":certitude})
                                else:
                                    if c2["code"] == code:
                                        print ("System and diagnosis code matched")
                                        records.append({"record":resc,"certitude":certitude})
    if len(records)==0:
        return {"status":"unavailable","certitude":{unavailable["certitude"]}}
    else:
        return {"status":"available","records":records,"certitude":max(map(lambda a:a["certitude"],records))}                   
                      
                    
                
    
