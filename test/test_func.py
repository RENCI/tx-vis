from pdsphenotypemapping import dispatcher

test_func():
    dispatcher.lookupFHIR("data", "1", [{"system":"", "code":""}])
    assert True
