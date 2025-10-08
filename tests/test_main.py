import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # დამატებულია path-ისთვის

from fastapi.testclient import TestClient
import main  # ძირეულიდან იმპორტი

client = TestClient(main.app)

def test_get_form():
    response = client.get("/")
    assert response.status_code == 200
    assert "სანომრე ნიშნების ვალიდაცია" in response.text

def test_is_valid():
    from main import is_valid
    assert is_valid("AB-123-CDE") == True
    assert is_valid("ab-123-cde") == False  # lowercase
    assert is_valid("AB123CDE") == False  # no dashes