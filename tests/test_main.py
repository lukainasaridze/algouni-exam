from fastapi.testclient import TestClient
# მთავარი შესწორება აქ არის: შედარებითი იმპორტი '..main' იცვლება პირდაპირი იმპორტით 'main'
from main import app, is_valid

client = TestClient(app)

def test_get_form():
    response = client.get("/")
    assert response.status_code == 200
    # უმჯობესია შეამოწმოთ რაიმე უფრო კონკრეტული, მაგალითად, სათაური
    assert '<h1 class="text-3xl font-bold mb-4">სანომრე ნიშნების ვალიდატორი</h1>' in response.text

def test_is_valid():
    # ეს იმპორტი უკვე ფაილის თავშია გაკეთებული
    assert is_valid("AB-123-CD") == True # სწორი 9-სიმბოლოიანი ფორმატი
    assert is_valid("AB-123-CDE") == False # ეს 10 სიმბოლოა, ამიტომ არასწორია
    assert is_valid("ab-123-cd") == False  # პატარა ასოები არასწორია
    assert is_valid("AB123CD") == False   # ტირეების გარეშე არასწორია
    assert is_valid("A1-123-CD") == False  # პირველი ნაწილი უნდა იყოს მხოლოდ ასოები
    assert is_valid("AB-12-CDE") == False  # შუა ნაწილი უნდა იყოს 3 ციფრი
