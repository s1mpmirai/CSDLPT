import urllib.request, json
import time

def test_api():
    base_url = 'http://localhost:5000/api'
    
    # Login
    print("Testing Login...")
    login_url = f'{base_url}/auth/login'
    data = json.dumps({'username': 'admin', 'password': 'admin123'}).encode()
    req = urllib.request.Request(login_url, data=data, headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req)
        r = json.loads(resp.read())
        token = r.get('token')
        if not token:
            print("Login failed: No token")
            return
        print("Login successful")
    except Exception as e:
        print(f"Login error: {e}")
        return

    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

    # 0. Seed Data
    print("\nSeeding Data...")
    try:
        req = urllib.request.Request(f'{base_url}/seed/all', data=b'', headers=headers, method='POST')
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        print(f"Seeding result: {data.get('message')}")
    except Exception as e:
        print(f"Seeding error: {e} (maybe already seeded)")
    print("\nTesting GET /api/departments...")
    try:
        req = urllib.request.Request(f'{base_url}/departments', headers=headers)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        print(f"Status: {resp.status}")
        if data.get('success'):
            depts = data.get('data', [])
            print(f"Found {len(depts)} departments")
            for d in depts:
                print(f" - {d.get('name')}: {d.get('employee_count')} employees")
        else:
            print(f"Failed: {data.get('message')}")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test Employees (filtered)
    print("\nTesting GET /api/employees?phongBan=1...")
    try:
        req = urllib.request.Request(f'{base_url}/employees?phongBan=1', headers=headers)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        print(f"Status: {resp.status}")
        if data.get('success'):
            items = data.get('data', {}).get('items', [])
            print(f"Found {len(items)} employees for department 1")
        else:
            print(f"Failed: {data.get('message')}")
    except Exception as e:
        print(f"Error: {e}")

    # 3. Test Report
    print("\nTesting GET /api/reports/payroll?month=2026-03...")
    try:
        req = urllib.request.Request(f'{base_url}/reports/payroll?month=2026-03', headers=headers)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        print(f"Status: {resp.status}")
        if data.get('success'):
            print(f"Report data: {data.get('data')}")
        else:
            print(f"Failed: {data.get('message')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_api()
