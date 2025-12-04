import requests

request = requests.post("http://127.0.0.1:8080/", json={"key": "value"})

if request.status_code == 200:
    print("Succes:", request.text)
else:
    print("Error:", request.status_code)
