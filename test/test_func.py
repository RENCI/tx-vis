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

def test_api_age():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=1000&clinical_feature_variable=age&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": 10,
        "calculation": "birthDate",
        "certitude": 2
    }
    
def test_api_age_no_field():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=1001&clinical_feature_variable=age&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": None,
        "calculation": "birthDate not set",
        "certitude": 0
    }
    
def test_api_age_no_record():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=2000&clinical_feature_variable=age&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": None,
        "calculation": "record not found",
        "certitude": 0
    }
    
def test_api_serum_creatinine():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=1000&clinical_feature_variable=2160-0&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": {'code': '%', 'system': 'http://unitsofmeasure.org', 'unit': '%', 'value': 95},
        "calculation": "from http://loinc.org 2160-0 at 2019-10-19T00:00:00Z",
        "certitude": 2
    }
      

def test_api_serum_creatinine_no_timestamp():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=1001&clinical_feature_variable=2160-0&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": {'code': '%', 'system': 'http://unitsofmeasure.org', 'unit': '%', 'value': 95},
        "calculation": "from http://loinc.org 2160-0 at notimestamp",
        "certitude": 1
    }


def test_api_serum_creatinine_no_record():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=2000&clinical_feature_variable=2160-0&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": None,
        "calculation": "from http://loinc.org 2160-0",
        "certitude": 0
    }

def test_api_bleeding():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=1000&clinical_feature_variable=HP:0001892&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": [],
        "calculation": "from http://hl7.org/fhir/sid/icd-10-cm I60.0011 at 2019-10-19T00:00:00Z",
        "certitude": 2
    }
      

def test_api_bleeding_no_timestamp():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=1001&clinical_feature_variable=HP:0001892&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": [],
        "calculation": "from http://hl7.org/fhir/sid/icd-10-cm I60.0011 at notimestamp",
        "certitude": 1
    }


def test_api_bleeding_no_record():
    result=requests.get("http://pdsphenotypemapping:8080/mapping?patient_id=2000&clinical_feature_variable=HP:0001892&timestamp=2019-10-19T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "value": None,
        "calculation": "from " + ",".join(map(lambda a: a["system"] + " " + a["code"], [
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
    }
