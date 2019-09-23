from pdsphenotypemapping import dispatcher
import requests

def test_func_pc1():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passcond1", "17944", [{"system":"http://hl7.org/fhir/sid/icd-10-cm", "code":"C50.021"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_pc2():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passcond2", "12595", [{"system":"http://hl7.org/fhir/sid/icd-9-cm", "code":"401.9"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_po1():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passobs1", "3533", [{"system":"http://loinc.org", "code":"7867677-4"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_po2():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passobs2", "55708", [{"system":"http://loinc.org", "code":"785-6"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_pb1():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passbleeding1", "13429", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"T85.830"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_pb2():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passbleeding2", "12250", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"H31.3"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_pg():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passpreg", "17937", [{"system":"http://hl7.org/fhir/sid/icd-10-cm", "code":"Z34.*"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_pk1():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passkidneys1", "18044", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"E11.2"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_pk2():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passkidneys2", "14518", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"T36.5X5"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_pcc1():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passcreatinine1", "3530", [{"system":"http://loinc.org", "code":"2160-0"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_pcc2():

    result=dispatcher.lookupFHIR("test/testcases/passcases/passcreatinine2", "66", [{"system":"http://loinc.org", "code":"2160-0"}])
    arraylen=len(result)
    assert arraylen!=0
def test_func_fo1():

    result=dispatcher.lookupFHIR("test/testcases/passcases/failobs1", "55708", [{"system":"http://loinc.org", "code":"2160-0"}])
    arraylen=len(result)
    assert arraylen==0
def test_func_fo2():

    result=dispatcher.lookupFHIR("test/testcases/passcases/failobs2", "14", [{"system":"http://loinc.org", "code":"2160-0"}])
    arraylen=len(result)
    assert arraylen==0
def test_func_fc1():

    result=dispatcher.lookupFHIR("test/testcases/passcases/failcond1", "13429", [{"system":"http://loinc.org", "code":"2160-0"}])
    arraylen=len(result)
    assert arraylen==0
def test_func_fc2():

    result=dispatcher.lookupFHIR("test/testcases/passcases/failcond2", "14", [{"system":"http://loinc.org", "code":"2160-0"}])
    arraylen=len(result)
    assert arraylen==0


json_headers = {
    "Content-Type": "application/json"
}

import time
def test_api():
    result=requests.post("http://pdsphenotypemapping:8080/mapping", json={
        "input_dir": "test/testcases/passcases/passcond1",
        "patient_id": "17944",
        "codes": [{"system":"http://hl7.org/fhir/sid/icd-10-cm", "code":"C50.021"}]
    }, headers=json_headers)
    assert result.status_code == 200
    arraylen=len(result.json())
    assert arraylen!=0
    
      
