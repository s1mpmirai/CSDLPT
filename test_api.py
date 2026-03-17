import urllib.request, json

url = 'http://localhost:5000/api/auth/login'
data = json.dumps({'username': 'admin', 'password': 'admin123'}).encode()
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
r = json.loads(resp.read())
print('login', r)

if 'token' in r:
    token = r['token']
    req2 = urllib.request.Request('http://localhost:5000/api/statistics', headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'})
    resp2 = urllib.request.urlopen(req2)
    print('statistics', resp2.status, resp2.read().decode())