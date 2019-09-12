import json
import os 

def loadFHIR(input_file):
    return json.load(input_file)


def lookupFHIR(input_dir, patient_id, codes): # [{"system":"", "code":""}]
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
            
                if resc["resourceType"] == resc_type:
                    for c2 in resc["code"]["coding"]:
                        if c2["system"] == system and c2["code"] == code:
                            records.append(resc)
                            
                    
                
    
