import requests

# Test GET
response = requests.get("http://127.0.0.1:8000/notes")
assert response.status_code == 200
print("GET/notes berhasil")
# Test DELETE
response = requests.delete("http://127.0.0.1:8000/notes/999999")
assert response.status_code == 404
print("DELETE/notes/{id} - ID tidak ditemukan: berhasil")
# Test POST
response = requests.post(
    "http://127.0.0.1:8000/notes",
    json={
        "title": "Test API",
        "content": "Testing POST endpoint",
    },
)
assert response.status_code == 200
print("POST/notes berhasil")
# Test PUT
response = requests.put(
    "http://127.0.0.1:8000/notes/1",
    json={
        "content": "Content hasil testing PUT",
    },
)
assert response.status_code == 200
print("PUT/notes/{id} berhasil")
