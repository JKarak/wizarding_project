import requests

res = requests.get('http://127.0.0.1:5000/user/hihihiha/pamparam/auth',
              headers={'Content-Type': 'application/json'})
print(res)