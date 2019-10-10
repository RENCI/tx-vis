import json
import os
import re

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
    
    mpg={
        "serum creatinine":[{
            "system":"http://loinc.org",
            "code":"2160-0",
            "is_regex":False
            }],
        "pregnancy":[{
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Z34\\.",
            "is_regex":True
            }],
        "bleeding":[{
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
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H26.6",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H27.0",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H27.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H27.4",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H27.6",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H28.0",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H28.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H28.4",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"H28.6",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K29.01",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K31.811",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K92.0",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K55.21",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.01",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.21",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.31",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.33",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.41",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.51",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.53",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.81",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.91",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K57.93",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K62.5",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K92.1",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K92.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"K66.1",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"M25.0",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I31.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^R58\\.",
            "is_regex":True            
            }],
        "kidney dysfunction":[{
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N00\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N10\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N17\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N14\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N14.1",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"N14.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"T36.5X5",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"B52.0",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"D59.3",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"E10.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"E11.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"E13.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^I12\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^I13\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I15.1",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"I15.2",
            "is_regex":False            
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N01\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N02\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N03\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N04\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N05\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N06\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N07\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N08\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N11\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N13\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N15\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N16\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N18\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N19\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N25\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N26\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N27\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N28\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N29\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Q60\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Q61\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Q62\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Q63\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^Z49\\.",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"Z99.2",
            "is_regex":True 
            },
            {
            "system":"http://hl7.org/fhir/sid/icd-10-cm",
            "code":"^N12\\.",
            "is_regex":True 
            }]
        }
    
    codes=mpg[clinical]
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
            
def lookupFHIR(input_dir, patient_id, codes): # 'codes' parameter is a list of [{"system":"", "code":""}]
    records = []
    for root, _, fnames in os.walk(input_dir, topdown=True):
        for f in fnames:
            resc = loadFHIR(os.path.join(root,f))
            for c in codes:  
                system = c["system"]
                code = c["code"]
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
                                        records.append(resc)
                                else:
                                    if c2["code"] == code:
                                        print ("System and diagnosis code matched")
                                        records.append(resc)
    return records                            
                      
                    
                
    
