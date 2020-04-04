from util.is_call import is_call

def test_is_call():
    assert is_call("CALL") == True

def test_is_call_short():
    assert is_call("C") == True

def test_is_put():
    assert is_call("PUT") == False

def test_is_put_short():
    assert is_call("P") == False
