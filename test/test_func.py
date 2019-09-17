from pdsphenotypemapping import dispatcher

def test_func():
    dispatcher.lookupFHIR("testcases/fail", "14518", [{"system":"http://hl7.org/fhir/sid/icd-10", "code":"T36.5X5"}])
    assert True
