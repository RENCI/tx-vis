patients = {
    "1000": {
        "birthDate": "2009-01-01",
        "gender": "male"
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
                    "unit": "mg/dL",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg/dL"
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
                    "unit": "mg/dL",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg/dL"
                }
            }
        },{
            "resource":{
                "resourceType": "Observation",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "29463-7"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/1000"
                },
                "effectiveInstant": "2019-10-19T00:00:00Z",
                "valueQuantity": {
                    "value": 99.9,
                    "unit": "kg",
                    "system": "http://unitsofmeasure.org",
                    "code": "kg"
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
                    "unit": "mg/dL",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg/dL"
                }
            }
        },{
            "resource":{
                "resourceType": "Observation",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "29463-7"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/1001"
                },
                "valueQuantity": {
                    "value": 99.9,
                    "unit": "kg",
                    "system": "http://unitsofmeasure.org",
                    "code": "kg"
                }
            }
        }]
    },
    "3000": {
        "resourceType": "Bundle",
        "entry": [{
            "resource": {
                "resourceType": "Observation",
                "subject": {
                    "reference": "Patient/3000"
                },
                "effectiveInstant": "2019-10-19T00:00:00Z",
                "valueQuantity": {
                    "value": 95,
                    "unit": "mg/dL",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg/dL"
                }
            }
        }]
    },
    "3001": {
        "resourceType": "Bundle",
        "entry": [{
            "resource": {
                "resourceType": "Observation",
                "subject": {
                    "reference": "Patient/3001"
                },
                "code": {
                },
                "effectiveInstant": "2019-10-19T00:00:00Z",
                "valueQuantity": {
                    "value": 95,
                    "unit": "mg/dL",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg/dL"
                }
            }
        }]
    },
    "5000": {
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
                    "unit": "mg/dL",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg/dL"
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
                    "unit": "mg/dL",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg/dL"
                }
            }
        },{
            "resource":{
                "resourceType": "Observation",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "29463-7"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/1000"
                },
                "effectiveInstant": "2019-10-19T00:00:00Z",
                "valueQuantity": {
                    "value": 99900,
                    "unit": "g",
                    "system": "http://unitsofmeasure.org",
                    "code": "g"
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


