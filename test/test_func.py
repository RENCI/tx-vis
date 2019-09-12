from pdsphenotypemapping import dispatcher

def test_func():
    dispatcher.lookupFHIR("test/data", "1", [{"system":"", "code":""}])
    assert True
