from util.is_put import is_put

def test_is_call():
    assert is_put("CALL") == False

def test_is_call_short():
    assert is_put("C") == False

def test_is_put():
    assert is_put("PUT") == True

def test_is_put_short():
    assert is_put("P") == True
