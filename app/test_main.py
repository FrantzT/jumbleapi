from fastapi.testclient import TestClient
from .main import app 

client = TestClient(app)

# main test with a valid input value
def test_read_main():
    response = client.get("/api/jumble/?word=test")
    assert response.status_code == 200
    print(response.json())
    jumble_response = response.json()
    # as the returned value is a random string not matching input value
    # testing the response's type as it should return string 
    assert type(jumble_response["jumbled_word"]) == str 
    
# test verifing word doesn't include digits
def test_read_dig():
    response = client.get("/api/jumble/?word=test1")
    assert response.status_code == 422
    
# test verifing if the value is a word not a single character or digit
def test_read_short():
    response = client.get("/api/jumble/?word=1")
    assert response.status_code == 422
    
# test response from endpoint /api/audit/
def test_read_audit():
    response = client.get("/api/audit/")
    assert response.status_code == 200

