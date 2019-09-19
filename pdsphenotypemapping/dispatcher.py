import json
import os 

# function for loading patient record file(s)

def loadFHIR(input_file):
    with open(input_file) as inp_file:
        return json.load(inp_file)

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

                if resc["resourceType"] == resc_type:
                    print ("resource type matched")
                    for c2 in resc["code"]["coding"]: # compares system and diagnosis codes
                        if c2["system"] == system and c2["code"] == code:  
                            print ("System and diagnosis code matched")
                            pid = resc["subject"]["reference"].split("/") # compares patient_ids
                            if patient_id == pid[1]:
                                print("patient found")
                                records.append(resc)
    return records                            
                    
                
    
