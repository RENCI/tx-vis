patients = {
    "1000": {
        "birthDate": "2009-01-01"
    },
    "1001": {
        # "birthDate": "2009-01-01"
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
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "2160-0",
                            "display": "Creatinine [Mass/volume] in Serum or Plasma"
                        }
                    ]
                },
                "effectiveInstant": "2019-10-19T00:00:00Z",
                "valueQuantity": {
                    "value": 95,
                    "unit": "%",
                    "system": "http://unitsofmeasure.org",
                    "code": "%"
                }
            }
        }, {
            "resource": {
                "resourceType": "Observation",
                "subject": {
                    "reference": "Patient/1000"
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "2160-0",
                            "display": "Creatinine [Mass/volume] in Serum or Plasma"
                        }
                    ]
                },
                "effectiveInstant": "2019-01-01T00:00:00Z",
                "valueQuantity": {
                    "value": 90,
                    "unit": "%",
                    "system": "http://unitsofmeasure.org",
                    "code": "%"
                }
            }
        }]
    },
    "1001": {
        "resourceType": "Bundle",
        "entry": [{
            "resource": {
                "resourceType": "Observation",
                "subject": {
                    "reference": "Patient/1001"
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "2160-0",
                            "display": "Creatinine [Mass/volume] in Serum or Plasma"
                        }
                    ]
                },
                "valueQuantity": {
                    "value": 95,
                    "unit": "%",
                    "system": "http://unitsofmeasure.org",
                    "code": "%"
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
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "I60.0011"
                        }
                    ]
                },
                "onsetDateTime": "2019-10-19T00:00:00Z"
            }
        }]
    },
    "1001": {
        "resourceType": "Bundle",
        "entry": [{
            "resource": {
                "resourceType": "Condition",
                "subject": {
                    "reference": "Patient/1001"
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": "I60.0011",
                        }
                    ]
                }
            }
        }]
    }
}

def get_patient(patient_id):
    return patients.get(patient_id, ("Not Found", 404))

def get_observation(patient):
    return observations.get(patient, {"resourceType":"Bundle"})

def get_condition(patient):
    return conditions.get(patient, {"resourceType":"Bundle"})


