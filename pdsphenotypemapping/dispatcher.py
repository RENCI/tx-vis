import json
import os 

# function for loading patient record file(s)

def loadFHIR(input_file): 
    return json.load(input_file)

def lookupFHIR(input_dir, patient_id, codes): # 'codes' parameter is a list of [{"system":"", "code":""}]
    records = []
    for root, _, fnames in os.walk(input_dir, topdown=True):
        for f in fnames:
            resc = loadFHIR(os.path.join(root, f))
            for c in codes:  
                system = c["system"]
                code = c["code"]
                if system == "http://loinc.org":
                    resc_type = "Observation"
                elif system == "http://hl7.org/fhir/sid/icd-10":
                    resc_type = "Condition"
                elif system == "http://hl7.org/fhir/sid/icd-9-cm":
                    resc_type = "Condition"
                else:
                    print ("Unknown resource type")

                if resc["resourceType"] == resc_type:
                    for c2 in resc["code"]["coding"]: # compares system and diagnosis codes
                        if c2["system"] == system and c2["code"] == code:  
                            for p in patient_id: # compares patient_ids
                                pid = resc["subject"]["reference"].split("/")
                                if p == pid[1]:
                                    records.append(resc)
                                    return records                            
                    
                
    
