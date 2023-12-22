from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_new_diagnose():
    new_diagnose_data = {
        "name": "Test Diagnosis",
        "description": "Test Description"
    }

    response = client.post("/diagnose/create_diag", json=new_diagnose_data)
    
    assert response.status_code == 200
    
    created_diagnose = response.json()

    assert created_diagnose["name"] == new_diagnose_data["name"]
    assert created_diagnose["description"] == new_diagnose_data["description"]


def test_get_diagnose_by_id():

    
    response = client.get("/diagnose/get_by_id/1")
    assert response.status_code == 200
    
    assert response.json() == {"name": "Test Diagnosis"}
    
    response = client.get("/diagnose/get_by_id/2")
    assert response.status_code == 404
