# from pdsphenotypemapping import dispatcher
import requests

# def test_func_pc1():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passcond1", "17944", [{"system":"http://hl7.org/fhir/sid/icd-10-cm", "code":"C50.021"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_pc2():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passcond2", "12595", [{"system":"http://hl7.org/fhir/sid/icd-9-cm", "code":"401.9"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_po1():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passobs1", "3533", [{"system":"http://loinc.org", "code":"7867677-4"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_po2():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passobs2", "55708", [{"system":"http://loinc.org", "code":"785-6"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_pb1():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passbleeding1", "13429", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"T85.830"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_pb2():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passbleeding2", "12250", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"H31.3"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_pg():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passpreg", "17937", [{"system":"http://hl7.org/fhir/sid/icd-10-cm", "code":"Z34.*"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_pk1():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passkidneys1", "18044", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"E11.2"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_pk2():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passkidneys2", "14518", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"T36.5X5"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_pcc1():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passcreatinine1", "3530", [{"system":"http://loinc.org", "code":"2160-0"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_pcc2():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/passcreatinine2", "66", [{"system":"http://loinc.org", "code":"2160-0"}])
#     arraylen=len(result)
#     assert arraylen!=0
# def test_func_fo1():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/failobs1", "55708", [{"system":"http://loinc.org", "code":"2160-0"}])
#     arraylen=len(result)
#     assert arraylen==0
# def test_func_fo2():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/failobs2", "14", [{"system":"http://loinc.org", "code":"2160-0"}])
#     arraylen=len(result)
#     assert arraylen==0
# def test_func_fc1():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/failcond1", "13429", [{"system":"http://loinc.org", "code":"2160-0"}])
#     arraylen=len(result)
#     assert arraylen==0
# def test_func_fc2():

#     result=dispatcher.lookupFHIR("test/testcases/passcases/failcond2", "14", [{"system":"http://loinc.org", "code":"2160-0"}])
#     arraylen=len(result)
#     assert arraylen==0


json_headers = {
    "Accept": "application/json"
}


def query(pid, cv, unit=None):
    q = {
        "clinical_feature_variable": cv
    }
    if unit is not None:
        q["unit"] = unit
    return requests.post(f"http://pdsphenotypemapping:8080/mapping?patient_id={pid}&timestamp=2019-10-19T00:00:00Z&data_provider_plugin_id=dpi", headers=json_headers, json=[q])


def query_from_data(pid, cv, data, unit=None):
    q = {
        "clinical_feature_variable": cv
    }
    if unit is not None:
        q["unit"] = unit
    q["data"] = data
    return requests.post(f"http://pdsphenotypemapping:8080/mappingFromRecords?timestamp=2019-10-19T00:00:00Z", headers=json_headers, json=[q])


def test_api_age():
    result = query("1000", "LOINC:30525-0")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 10,
        "unit": "year",
        "calculation": "Current date '2019-10-19' minus patient's birthdate (FHIR resource 'Patient' field>'birthDate' = '2009-01-01T00:00:00Z')",
        "certitude": 2
    }]

    
def test_api_age_no_field():
    result = query("1001", "LOINC:30525-0")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": None,
        "calculation": "birthDate not set",
        "certitude": 0
    }]

    
def test_api_age_no_record():
    result = query("2000", "LOINC:30525-0")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": None,
        "calculation": "record not found",
        "certitude": 0
    }]

    
def test_api_age_unit_year():
    result = query("1000", "LOINC:30525-0", "year")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 10,
        "unit": "year",
        "calculation": "Current date '2019-10-19' minus patient's birthdate (FHIR resource 'Patient' field>'birthDate' = '2009-01-01T00:00:00Z')",
        "certitude": 2
    }]

    
def test_api_age_unit_wrong():
    result = query("1000", "LOINC:30525-0", "wrong")
    print(result.content)
    assert result.status_code == 400
                
    assert result.json() == "unsupported unit wrong"

    
def test_api_sex():
    result = query("1000", "LOINC:21840-4")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": "male",
        "calculation": "FHIR resource 'Patient' field>'gender' = male",
        "certitude": 2
    }]

    
def test_api_sex_no_field():
    result = query("1001", "LOINC:21840-4")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": None,
        "calculation": "gender not set",
        "certitude": 0
    }]

    
def test_api_sex_no_record():
    result = query("2000", "LOINC:21840-4")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": None,
        "calculation": "record not found",
        "certitude": 0
    }]

    
def test_api_serum_creatinine():
    result = query("1000", "LOINC:2160-0")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 95,
        "unit": "mg/dL",
        "calculation": "current as of 2019-10-19T00:00:00Z. (Date computed from FHIR resource 'Observation', field>'effectiveInstant' = '2019-10-19T00:00:00Z'); 'serum creatinine' computed from FHIR resource 'Observation' code http://loinc.org 2160-0, field>'valueQuantity'field>'value' = '95', 'unit'>'mg/dL'.",
        "timestamp": "2019-10-19T00:00:00Z",
        "certitude": 2
    }]
      

def test_api_serum_creatinine_no_timestamp():
    result = query("1001", "LOINC:2160-0")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 95,
        "unit": "mg/dL",
        "calculation": "current as of 2019-10-19T00:00:00Z. (record has no timestamp) 'serum creatinine' computed from FHIR resource 'Observation' code http://loinc.org 2160-0, field>'valueQuantity'field>'value' = '95', 'unit'>'mg/dL'.",
        "timestamp": None,
        "certitude": 1
    }]


def test_api_serum_creatinine_no_record():
    result = query("2000", "LOINC:2160-0")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": None,
        "calculation": "no record found code http://loinc.org 2160-0",
        "certitude": 0
    }]

    
def test_api_no_code():
    result = query("3000", "LOINC:2160-0")
    print(result.content)
    assert result.status_code == 500
                
    assert result.json() == {
        "error": "malformated record: no code",
        "record": {
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
    }

    
def test_api_no_coding_under_code():
    result = query("3001", "LOINC:2160-0")
    print(result.content)
    assert result.status_code == 500
                
    assert result.json() == {
        "error": "malformated record: no coding under code",
        "record": {
            "resourceType": "Observation",
            "subject": {
                "reference": "Patient/3001"
            },
            "code": {},
            "effectiveInstant": "2019-10-19T00:00:00Z",
            "valueQuantity": {
                "value": 95,
                "unit": "mg/dL",
                "system": "http://unitsofmeasure.org",
                "code": "mg/dL"
            }
        }
    }

    
def test_api_weight():
    result = query("1000", "LOINC:29463-7")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 99.9,
        "unit": "kg",
        "calculation": "current as of 2019-10-19T00:00:00Z. (Date computed from FHIR resource 'Observation', field>'effectiveInstant' = '2019-10-19T00:00:00Z'); 'weight' computed from FHIR resource 'Observation' code http://loinc.org 29463-7, field>'valueQuantity'field>'value' = '99.9', 'unit'>'kg'.",
        "timestamp": "2019-10-19T00:00:00Z",
        "certitude": 2
    }]
      

def test_api_weight_no_timestamp():
    result = query("1001", "LOINC:29463-7")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 99.9,
        "unit": "kg",
        "calculation": "current as of 2019-10-19T00:00:00Z. (record has no timestamp) 'weight' computed from FHIR resource 'Observation' code http://loinc.org 29463-7, field>'valueQuantity'field>'value' = '99.9', 'unit'>'kg'.",
        "timestamp": None,
        "certitude": 1
    }]


def test_api_weight_no_record():
    result = query("2000", "LOINC:29463-7")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": None,
        "calculation": "no record found code http://loinc.org 29463-7",
        "certitude": 0
    }]

    
def test_api_weight_unit_kg():
    result = query("1000", "LOINC:29463-7", "kg")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 99.9,
        "unit": "kg",
        "calculation": "current as of 2019-10-19T00:00:00Z. (Date computed from FHIR resource 'Observation', field>'effectiveInstant' = '2019-10-19T00:00:00Z'); 'weight' computed from FHIR resource 'Observation' code http://loinc.org 29463-7, field>'valueQuantity'field>'value' = '99.9', 'unit'>'kg'.",
        "timestamp": "2019-10-19T00:00:00Z",
        "certitude": 2
    }]

    
def test_api_weight_unit_g():
    result = query("1000", "LOINC:29463-7", "g")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 99900,
        "unit": "g",
        "calculation": "current as of 2019-10-19T00:00:00Z. (Date computed from FHIR resource 'Observation', field>'effectiveInstant' = '2019-10-19T00:00:00Z'); 'weight' computed from FHIR resource 'Observation' code http://loinc.org 29463-7, field>'valueQuantity'field>'value' = '99.9', 'unit'>'kg' converted to g.",
        "timestamp": "2019-10-19T00:00:00Z",
        "certitude": 2
    }]

    
def test_api_weight_unit_code_from_data():
    result = query_from_data("1000", "LOINC:29463-7", [{
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
            "code": "kg"
        }
    }])
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 99.9,
        "unit": "kg",
        "calculation": "current as of 2019-10-19T00:00:00Z. (Date computed from FHIR resource 'Observation', field>'effectiveInstant' = '2019-10-19T00:00:00Z'); 'weight' computed from FHIR resource 'Observation' code http://loinc.org 29463-7, field>'valueQuantity'field>'value' = '99.9', 'code'>'kg'.",
        "timestamp": "2019-10-19T00:00:00Z",
        "certitude": 2
    }]

    
def test_api_weight_unit_system_default():
    result = query("5000", "LOINC:29463-7")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 99.9,
        "unit": "kg",
        "calculation": "current as of 2019-10-19T00:00:00Z. (Date computed from FHIR resource 'Observation', field>'effectiveInstant' = '2019-10-19T00:00:00Z'); 'weight' computed from FHIR resource 'Observation' code http://loinc.org 29463-7, field>'valueQuantity'field>'value' = '99900', 'unit'>'g' converted to kg.",
        "timestamp": "2019-10-19T00:00:00Z",
        "certitude": 2
    }]

    
def test_api_weight_unit_wrong():
    result = query("1000", "LOINC:29463-7", "wrong")
    print(result.content)
    assert result.status_code == 500
                
    assert result.json() == "'wrong' is not defined in the unit registry"

    
def test_api_bleeding():
    result = query("1000", "HP:0001892")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": True,
        "calculation": "current as of 2019-10-19T00:00:00Z. (Date computed from FHIR resource 'Condition', field>'onsetDateTime' = '2019-10-19T00:00:00Z'); 'bleeding' computed from FHIR resource 'Condition' code http://hl7.org/fhir/sid/icd-10-cm I60.0011.",
        "timestamp": "2019-10-19T00:00:00Z",
        "certitude": 2
    }]
      

def test_api_bleeding_no_timestamp():
    result = query("1001", "HP:0001892")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": True,
        "calculation": "current as of 2019-10-19T00:00:00Z. (record has no timestamp) 'bleeding' computed from FHIR resource 'Condition' code http://hl7.org/fhir/sid/icd-10-cm I60.0011.",
        "timestamp": None,
        "certitude": 1
    }]


def test_api_bleeding_no_record():
    result = query("2000", "HP:0001892")
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": None,
        "calculation": "no record found code " + ",".join(map(lambda a: a["system"] + " " + a["code"], [
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
        ])),
        "certitude": 0
    }]


def test_api_age_from_data():
    result = query_from_data("1000", "LOINC:30525-0", {"birthDate":"2009-01-01"})
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 10,
        "unit": "year",
        "calculation": "Current date '2019-10-19' minus patient's birthdate (FHIR resource 'Patient' field>'birthDate' = '2009-01-01')",
        "certitude": 2
    }]

    
def test_api_sex_from_data():
    result = query_from_data("1000", "LOINC:21840-4", {"gender": "male"})
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": "male",
        "calculation": "FHIR resource 'Patient' field>'gender' = male",
        "certitude": 2
    }]

    
def test_api_serum_creatinine_from_data():
    result = query_from_data("1000", "LOINC:2160-0", [{
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
    }])
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [{
        "value": 95,
        "unit": "mg/dL",
        "calculation": "current as of 2019-10-19T00:00:00Z. (Date computed from FHIR resource 'Observation', field>'effectiveInstant' = '2019-10-19T00:00:00Z'); 'serum creatinine' computed from FHIR resource 'Observation' code http://loinc.org 2160-0, field>'valueQuantity'field>'value' = '95', 'unit'>'mg/dL'.",
        "timestamp": "2019-10-19T00:00:00Z",
        "certitude": 2
    }]
