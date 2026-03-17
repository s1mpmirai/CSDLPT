import urllib.request, json

# First login
url = 'http://localhost:5000/api/auth/login'
data = json.dumps({'username': 'admin', 'password': 'admin123'}).encode()
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
r = json.loads(resp.read())
print('login', r)

if 'token' in r:
    token = r['token']
    # Test employees
    req3 = urllib.request.Request('http://localhost:5000/api/employees', headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'})
    resp3 = urllib.request.urlopen(req3)
    print('employees', resp3.status, resp3.read().decode())