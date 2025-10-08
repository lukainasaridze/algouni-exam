import pytest
from fastapi.testclient import TestClient
from main import app, is_valid

client = TestClient(app)

def test_get_form():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_is_valid():
    # Valid plates (9 characters: AA-999-RR)
    assert is_valid("AA-999-RR") == True
    assert is_valid("XY-123-ZW") == True
    assert is_valid("AB-000-CD") == True
    
    # Invalid plates
    assert is_valid("aa-999-rr") == False  # lowercase
    assert is_valid("AA999RR") == False    # no dashes
    assert is_valid("AA-99-RR") == False   # only 2 digits
    assert is_valid("AA-9999-RR") == False # 4 digits
    assert is_valid("A1-999-RR") == False  # digit in first part
    assert is_valid("AA-999-R1") == False  # digit in last part
    assert is_valid("AA-999-RRR") == False # 3 letters at end
    assert is_valid("AAA-999-RR") == False # 3 letters at start
    assert is_valid("AA_999_RR") == False  # underscores instead of dashes

def test_validate_plates_csv():
    csv_content = b"AA-999-RR\naa-999-rr\nXY-123-ZW\nINVALID"
    
    response = client.post(
        "/validate-plates/",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )
    
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "validated_plates.csv" in response.headers["content-disposition"]

def test_invalid_file_type():
    response = client.post(
        "/validate-plates/",
        files={"file": ("test.txt", b"content", "text/plain")}
    )
    
    assert response.status_code == 400