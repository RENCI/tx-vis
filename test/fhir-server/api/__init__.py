patients = {
    "1000": {
        "birthDate": "2009-01-01"
    }
}

observations = {
    "1000": {
        "resourceType": "Bundle",
        "entry": [{
            "resource": {
                "resourceType": "Observation",
                "subject": {
                    "reference": "Patient/1000"
                }
            }
        }]
    }
}

conditions = {
    "1000": {
        "resourceType": "Bundle",
        "entry": [{
            "resource": {
                "resourceType": "Condition",
                "subject": {
                    "reference": "Patient/1000"
                }
            }
        }]
    }
}

def get_patient(patient_id):
    return patients.get(patient_id)

def get_observation(patient_id):
    return observations.get(patient_id)

def get_condition(patient_id):
    return conditions.get(patient_id)


