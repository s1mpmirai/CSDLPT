# 🔌 Hướng dẫn Sử dụng API cho Frontend

## 📋 Tóm tắt API

**Base URL:** `http://localhost:5000` (development)

**Authentication:** Bearer Token (JWT)

**Headers:** 
```
Authorization: Bearer {token}
Content-Type: application/json
```

---

## 🔐 1. Authentication Flow

### Step 1: Login (Lấy Token)

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "username": "admin",
    "name": "Admin User",
    "role": "admin"
  }
}
```

### Step 2: Lưu Token (trong file, database, hoặc session)

```python
# Python
import requests
import json

response = requests.post(
    'http://localhost:5000/api/auth/login',
    json={'username': 'admin', 'password': 'admin123'}
)

data = response.json()
token = data['token']
user = data['user']

# Lưu token vào file.txt hoặc config (tạm thời)
with open('token.txt', 'w') as f:
    f.write(token)

# Hoặc save vào config dict
config = {'token': token, 'user': user}
```

### Step 3: Dùng Token trong Requests

```python
import requests

token = open('token.txt', 'r').read().strip()

response = requests.get(
    'http://localhost:5000/api/nhanvien',
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
)

data = response.json()
print(data)
```

---

## 🚀 2. API Endpoints (Đầy đủ)

### 🔑 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login & lấy token |
| GET | `/api/auth/me` | Lấy info user hiện tại |
| POST | `/api/auth/logout` | Logout |

### 👥 Nhân Viên (Employees)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/nhanvien` | Danh sách nhân viên | Admin/Kế toán |
| GET | `/api/nhanvien/{id}` | Chi tiết nhân viên | Admin/Kế toán |
| POST | `/api/nhanvien` | Thêm nhân viên | Admin only |
| PUT | `/api/nhanvien/{id}` | Cập nhật nhân viên | Admin only |
| DELETE | `/api/nhanvien/{id}` | Xóa nhân viên (soft) | Admin only |

### 💰 Lương (Payroll)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/luong/{id}` | Bảng lương nhân viên | Admin/Kế toán |
| PUT | `/api/luong/{id}` | Cập nhật bảng lương | Admin only |
| POST | `/api/luong/chi-tiet` | Tính lương tháng | Admin/Kế toán |
| GET | `/api/luong/chi-tiet/{id}` | Chi tiết lương tháng | Admin/Kế toán |
| GET | `/api/luong/danh-sach` | Danh sách lương tháng | Admin/Kế toán |

### 🏢 Phòng Ban (Departments)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/phongban` | Danh sách phòng ban | All |
| GET | `/api/phongban/{id}` | Chi tiết phòng ban | All |
| POST | `/api/phongban` | Thêm phòng ban | Admin only |
| PUT | `/api/phongban/{id}` | Cập nhật phòng ban | Admin only |

### 📌 Chức Vụ (Positions)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/chucvu` | Danh sách chức vụ | All |
| GET | `/api/chucvu/{id}` | Chi tiết chức vụ | All |
| POST | `/api/chucvu` | Thêm chức vụ | Admin only |
| PUT | `/api/chucvu/{id}` | Cập nhật chức vụ | Admin only |

---

## 💻 3. Code Examples - Python

### Setup: Install Requirements

```bash
pip install requests python-dotenv
```

**hoặc dùng async:**
```bash
pip install aiohttp python-dotenv
```

---

### Synchronous (Requests Library)

#### Login
```python
import requests
from typing import Dict

def login(username: str, password: str) -> Dict:
    """Login và nhận token"""
    response = requests.post(
        'http://localhost:5000/api/auth/login',
        json={'username': username, 'password': password}
    )
    
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.text}")
    
    data = response.json()
    
    # Lưu token
    with open('token.txt', 'w') as f:
        f.write(data['token'])
    
    return data['user']

# Usage
user = login('admin', 'admin123')
print(f"Logged in as {user['name']}")
```

#### Get Employees
```python
def get_employees(page: int = 1, limit: int = 20) -> list:
    """Lấy danh sách nhân viên"""
    # Đọc token từ file
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    
    response = requests.get(
        'http://localhost:5000/api/nhanvien',
        params={'page': page, 'limit': limit},
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch employees: {response.text}")
    
    return response.json()['data']

# Usage
employees = get_employees()
for emp in employees:
    print(f"{emp['maNV']}: {emp['tenNV']} ({emp['tenPhong']})")
```

#### Add Employee
```python
def add_employee(employee_data: dict) -> dict:
    """Thêm nhân viên mới"""
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    
    response = requests.post(
        'http://localhost:5000/api/nhanvien',
        json=employee_data,
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to add employee: {response.text}")
    
    return response.json()

# Usage
new_employee = {
    'tenNV': 'Trần Văn Test',
    'ngaySinh': '1998-05-15',
    'gioiTinh': 'Nam',
    'diaChi': '456 Đường XYZ',
    'sdt': '0912345678',
    'email': 'tranthitest@company.com',
    'maPhong': 1,
    'maChucVu': 3,
    'ngayVaoLam': '2024-01-01'
}

result = add_employee(new_employee)
print(f"Employee added: {result}")
```

#### Update Employee
```python
def update_employee(emp_id: int, update_data: dict) -> dict:
    """Cập nhật thông tin nhân viên"""
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    
    response = requests.put(
        f'http://localhost:5000/api/nhanvien/{emp_id}',
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to update employee: {response.text}")
    
    return response.json()

# Usage
result = update_employee(1, {'tenNV': 'Nguyễn Văn A - Updated'})
print(result)
```

#### Delete Employee
```python
def delete_employee(emp_id: int) -> dict:
    """Xóa nhân viên (soft delete)"""
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    
    response = requests.delete(
        f'http://localhost:5000/api/nhanvien/{emp_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to delete employee: {response.text}")
    
    return response.json()
```

---

### API Client Class (Better Practice)

```python
import requests
import json
from typing import Optional, Dict, Any

class PayrollAPIClient:
    """Client cho Payroll API"""
    
    def __init__(self, base_url: str = 'http://localhost:5000'):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user: Optional[Dict] = None
        self.session = requests.Session()
    
    def _load_token(self) -> Optional[str]:
        """Load token từ file"""
        try:
            with open('token.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
    
    def _save_token(self, token: str):
        """Save token vào file"""
        with open('token.txt', 'w') as f:
            f.write(token)
    
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Gọi API request"""
        url = f'{self.base_url}{endpoint}'
        
        # Thêm token nếu có
        headers = kwargs.get('headers', {})
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        headers['Content-Type'] = 'application/json'
        kwargs['headers'] = headers
        
        response = self.session.request(method, url, **kwargs)
        
        if response.status_code == 401:
            raise Exception('Unauthorized - Token expired, please login again')
        
        if response.status_code >= 400:
            raise Exception(f'API Error {response.status_code}: {response.text}')
        
        return response.json()
    
    def login(self, username: str, password: str) -> Dict:
        """Login"""
        data = self._request(
            'POST',
            '/api/auth/login',
            json={'username': username, 'password': password}
        )
        
        self.token = data['token']
        self.user = data['user']
        self._save_token(self.token)
        
        return self.user
    
    def get_user_info(self) -> Dict:
        """Lấy info user hiện tại"""
        return self._request('GET', '/api/auth/me')
    
    def logout(self):
        """Logout"""
        self._request('POST', '/api/auth/logout')
        self.token = None
        self.user = None
    
    # ===== Employees =====
    def get_employees(self, page: int = 1, limit: int = 20) -> Dict:
        """Danh sách nhân viên"""
        return self._request(
            'GET',
            '/api/nhanvien',
            params={'page': page, 'limit': limit}
        )
    
    def get_employee(self, emp_id: int) -> Dict:
        """Chi tiết nhân viên"""
        return self._request('GET', f'/api/nhanvien/{emp_id}')
    
    def create_employee(self, employee_data: Dict) -> Dict:
        """Thêm nhân viên"""
        return self._request('POST', '/api/nhanvien', json=employee_data)
    
    def update_employee(self, emp_id: int, data: Dict) -> Dict:
        """Cập nhật nhân viên"""
        return self._request('PUT', f'/api/nhanvien/{emp_id}', json=data)
    
    def delete_employee(self, emp_id: int) -> Dict:
        """Xóa nhân viên"""
        return self._request('DELETE', f'/api/nhanvien/{emp_id}')
    
    # ===== Payroll =====
    def get_salary_master(self, emp_id: int) -> Dict:
        """Bảng lương"""
        return self._request('GET', f'/api/luong/{emp_id}')
    
    def update_salary_master(self, emp_id: int, data: Dict) -> Dict:
        """Cập nhật bảng lương"""
        return self._request('PUT', f'/api/luong/{emp_id}', json=data)
    
    def calculate_payroll(self, thang: int, nam: int, maNV: Optional[int] = None) -> Dict:
        """Tính lương"""
        payload = {'thang': thang, 'nam': nam}
        if maNV:
            payload['maNV'] = maNV
        
        return self._request('POST', '/api/luong/chi-tiet', json=payload)
    
    def get_payroll_detail(self, emp_id: int, thang: int, nam: int) -> Dict:
        """Chi tiết lương tháng"""
        return self._request(
            'GET',
            f'/api/luong/chi-tiet/{emp_id}',
            params={'thang': thang, 'nam': nam}
        )
    
    def get_payroll_list(self, thang: int, nam: int) -> Dict:
        """Danh sách lương tháng"""
        return self._request(
            'GET',
            '/api/luong/danh-sach',
            params={'thang': thang, 'nam': nam}
        )
    
    # ===== Departments =====
    def get_departments(self) -> Dict:
        """Danh sách phòng ban"""
        return self._request('GET', '/api/phongban')
    
    def get_department(self, dept_id: int) -> Dict:
        """Chi tiết phòng ban"""
        return self._request('GET', f'/api/phongban/{dept_id}')
    
    def create_department(self, data: Dict) -> Dict:
        """Thêm phòng ban"""
        return self._request('POST', '/api/phongban', json=data)
    
    def update_department(self, dept_id: int, data: Dict) -> Dict:
        """Cập nhật phòng ban"""
        return self._request('PUT', f'/api/phongban/{dept_id}', json=data)
    
    # ===== Positions =====
    def get_positions(self) -> Dict:
        """Danh sách chức vụ"""
        return self._request('GET', '/api/chucvu')
    
    def get_position(self, pos_id: int) -> Dict:
        """Chi tiết chức vụ"""
        return self._request('GET', f'/api/chucvu/{pos_id}')
    
    def create_position(self, data: Dict) -> Dict:
        """Thêm chức vụ"""
        return self._request('POST', '/api/chucvu', json=data)
    
    def update_position(self, pos_id: int, data: Dict) -> Dict:
        """Cập nhật chức vụ"""
        return self._request('PUT', f'/api/chucvu/{pos_id}', json=data)

# Usage
client = PayrollAPIClient()

# Login
user = client.login('admin', 'admin123')
print(f"Logged in: {user['username']}")

# Get employees
employees = client.get_employees()
print(f"Total employees: {employees['total']}")
for emp in employees['data']:
    print(f"  - {emp['tenNV']} ({emp['tenPhong']})")

# Create new employee
new_emp = client.create_employee({
    'tenNV': 'Trần Văn Test',
    'ngaySinh': '1998-05-15',
    'gioiTinh': 'Nam',
    'diaChi': '456 Đường XYZ',
    'sdt': '0912345678',
    'email': 'tranthitest@company.com',
    'maPhong': 1,
    'maChucVu': 3,
    'ngayVaoLam': '2024-01-01'
})
print(f"Created: {new_emp}")

# Get payroll details
payroll = client.get_payroll_detail(1, 3, 2026)
print(f"Payroll: {payroll}")

# Logout
client.logout()
```

---

### Async/Await (aiohttp)

```python
import aiohttp
import asyncio
from typing import Dict, Optional

class AsyncPayrollClient:
    """Async client dùng aiohttp"""
    
    def __init__(self, base_url: str = 'http://localhost:5000'):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def _request(self, method: str, endpoint: str, **kwargs):
        """Gọi API request"""
        url = f'{self.base_url}{endpoint}'
        
        headers = kwargs.get('headers', {})
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        kwargs['headers'] = headers
        
        async with self.session.request(method, url, **kwargs) as response:
            if response.status >= 400:
                text = await response.text()
                raise Exception(f'API Error {response.status}: {text}')
            return await response.json()
    
    async def login(self, username: str, password: str) -> Dict:
        """Login"""
        data = await self._request(
            'POST',
            '/api/auth/login',
            json={'username': username, 'password': password}
        )
        self.token = data['token']
        return data['user']
    
    async def get_employees(self) -> Dict:
        """Danh sách nhân viên"""
        return await self._request('GET', '/api/nhanvien')
    
    async def get_payroll_list(self, thang: int, nam: int) -> Dict:
        """Danh sách lương"""
        return await self._request(
            'GET',
            '/api/luong/danh-sach',
            params={'thang': thang, 'nam': nam}
        )

# Usage
async def main():
    async with AsyncPayrollClient() as client:
        # Login
        user = await client.login('admin', 'admin123')
        print(f"Logged in: {user['username']}")
        
        # Get multiple data concurrently
        employees, payroll = await asyncio.gather(
            client.get_employees(),
            client.get_payroll_list(3, 2026)
        )
        
        print(f"Employees: {employees['total']}")
        print(f"Payroll records: {len(payroll['data'])}")

asyncio.run(main())
```

---

### Flask App Example (Python Frontend)

```python
# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from payroll_client import PayrollAPIClient

app = Flask(__name__)
app.secret_key = 'secret_key_here'

# Initialize client
api_client = PayrollAPIClient()

@app.route('/')
def index():
    if 'token' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            user = api_client.login(username, password)
            session['token'] = api_client.token
            session['user'] = user
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('login.html', error=str(e))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/employees')
def get_employees():
    try:
        api_client.token = session.get('token')
        data = api_client.get_employees()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/employees')
def employees():
    if 'token' not in session:
        return redirect(url_for('login'))
    return render_template('employees.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
```

---

## 📊 4. Query Parameters

### Danh sách nhân viên - Filtering & Pagination
```
GET /api/nhanvien?page=1&limit=20&trangThai=1

Parameters:
- page: trang thứ bao nhiêu (default: 1)
- limit: số record per page (default: 20)
- trangThai: trạng thái (1 = active, 0 = inactive)
```

### Danh sách lương tháng
```
GET /api/luong/danh-sach?thang=3&nam=2026

Parameters:
- thang: tháng (1-12)
- nam: năm
```

---

## ⚠️ 5. Error Handling - Python

### Status Codes
- `200 OK` - Thành công
- `400 Bad Request` - Dữ liệu invalid
- `401 Unauthorized` - Token không hợp lệ/hết hạn
- `403 Forbidden` - Không có quyền
- `404 Not Found` - Resource không tồn tại
- `422 Unprocessable Entity` - JWT validation error
- `500 Server Error` - Server error

### Xử lý Error - Python

```python
import requests
from requests.exceptions import RequestException, ConnectionError

def handle_api_error(func):
    """Decorator để handle API errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            print("Error: Cannot connect to API server")
            raise
        except RequestException as e:
            print(f"Request Error: {e}")
            raise
    return wrapper

@handle_api_error
def get_data_with_error_handling():
    token = open('token.txt', 'r').read().strip()
    
    response = requests.get(
        'http://localhost:5000/api/nhanvien',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    # Xử lý các status code khác nhau
    if response.status_code == 401:
        print("Token hết hạn - cần login lại")
        # Redirect to login or refresh token
        open('token.txt', 'w').write('')
        raise Exception("Token expired")
    
    elif response.status_code == 403:
        print("Bạn không có quyền truy cập tài nguyên này")
        raise PermissionError(response.json()['message'])
    
    elif response.status_code == 404:
        print("Tài nguyên không tồn tại")
        raise FileNotFoundError(response.json()['message'])
    
    elif response.status_code >= 500:
        print("Server error - vui lòng thử lại sau")
        raise Exception(f"Server Error: {response.status_code}")
    
    elif response.status_code >= 400:
        error_data = response.json()
        print(f"Client Error: {error_data.get('message', response.text)}")
        raise ValueError(error_data.get('message'))
    
    return response.json()

# Usage
try:
    data = get_data_with_error_handling()
    print(data)
except Exception as e:
    print(f"Failed: {e}")
```

---

## 🔗 6. CORS Configuration

**Backend đã cấu hình CORS cho tất cả origins:**
```python
CORS(app)  # Allow all origins in development
```

**Production:** Cần specify origins:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"]
    }
})
```

---

## 🧪 7. Test Accounts

```
admin / admin123         → Admin role (full access)
ketoan / ketoan123       → Kế toán role (view/edit lương)
nhanvien / nhanvien123   → Nhân viên role (view only)
```

---

## 📱 8. Python Frontend - Requirements & Setup

### Install Dependencies

```bash
# Cơ bản
pip install requests python-dotenv

# Async support
pip install aiohttp

# Web framework (nếu dùng Flask frontend)
pip install flask

# Database (optional - nếu cần local caching)
pip install sqlalchemy
```

### Project Structure

```
payroll-frontend/
├── payroll_client.py      # API client class
├── config.py              # Configuration
├── .env                   # Environment variables
├── token.txt              # Token cache (auto-generated)
├── main.py                # Script chính
├── app.py                 # Flask app (nếu dùng)
└── requirements.txt       # Dependencies
```

### requirements.txt

```
requests==2.31.0
python-dotenv==1.0.0
aiohttp==3.9.0
flask==2.3.3
```

---

## ✅ Python Frontend Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `payroll_client.py` (API client class)
- [ ] Create `config.py` with API_BASE_URL
- [ ] Create `.env` file (for credentials)
- [ ] Create login function (get token)
- [ ] Store token in file/session
- [ ] Add token to all authenticated requests
- [ ] Handle 401 errors (re-login)
- [ ] Add error handling & retry logic
- [ ] Implement employee operations (CRUD)
- [ ] Implement payroll calculations
- [ ] Add logging for debugging
- [ ] Test with all 3 test accounts
- [ ] Deploy to production

---

## 🚀 Quick Start - Python Frontend

### Bước 1: Setup Project

```bash
mkdir payroll-frontend
cd payroll-frontend

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# hoặc: source venv/bin/activate (Linux/macOS)

# Install dependencies
pip install requests python-dotenv
```

### Bước 2: Tạo API Client

Tạo file `payroll_client.py` - copy code từ **"API Client Class"** section ở trên

### Bước 3: Tạo Main Script

```python
# main.py
from payroll_client import PayrollAPIClient

# Khởi tạo client
client = PayrollAPIClient()

# Login
print("📝 Logging in...")
user = client.login('admin', 'admin123')
print(f"✅ Logged in: {user['username']}")

# Lấy danh sách nhân viên
print("\n📋 Fetching employees...")
employees = client.get_employees()
print(f"Total: {employees['total']} employees")
for emp in employees['data']:
    print(f"  - {emp['maNV']}: {emp['tenNV']} ({emp['tenPhong']})")

# Tính lương tháng 3/2026
print("\n💰 Calculating payroll for March 2026...")
payroll = client.calculate_payroll(3, 2026)
print(f"Calculated payroll: {payroll}")

# Logout
print("\n👋 Logging out...")
client.logout()
print("✅ Done!")
```

### Bước 4: Chạy

```bash
python main.py
```

Expected output:
```
📝 Logging in...
✅ Logged in: admin

📋 Fetching employees...
Total: 8 employees
  - 1: Nguyễn Văn A (Kỹ Thuật)
  - 2: Trần Thị B (Kế Toán)
  ...

💰 Calculating payroll for March 2026...
Calculated payroll: {...}

👋 Logging out...
✅ Done!
```

---

## 🌐 Flask Frontend App - Complete Example

```python
# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from payroll_client import PayrollAPIClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize client
api_client = PayrollAPIClient(os.getenv('API_BASE_URL', 'http://localhost:5000'))

@app.before_request
def load_token():
    """Load token từ session trước mỗi request"""
    token = session.get('token')
    if token:
        api_client.token = token

@app.route('/')
def index():
    if 'token' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            user = api_client.login(username, password)
            session['token'] = api_client.token
            session['user'] = user
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('login.html', error=str(e)), 400
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    api_client.logout()
    return redirect(url_for('login'))

@app.route('/employees')
def employees_page():
    if 'token' not in session:
        return redirect(url_for('login'))
    return render_template('employees.html')

@app.route('/api/employees')
def api_employees():
    try:
        data = api_client.get_employees(
            page=request.args.get('page', 1, type=int),
            limit=request.args.get('limit', 20, type=int)
        )
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/payroll')
def api_payroll():
    try:
        thang = request.args.get('thang', type=int)
        nam = request.args.get('nam', type=int)
        
        if not thang or not nam:
            return jsonify({'error': 'Missing thang or nam'}), 400
        
        data = api_client.get_payroll_list(thang, nam)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=8000)
```

---

## 💡 Pro Tips - Python API Usage

1. **Reuse Connection:**
   ```python
   # ✅ GOOD - Reuse session
   client = PayrollAPIClient()
   for i in range(10):
       data = client.get_employees()
   ```

2. **Async for Better Performance:**
   ```python
   # ✅ GOOD - Concurrent requests
   async with AsyncPayrollClient() as client:
       await client.login('admin', 'admin123')
       emp, payroll = await asyncio.gather(
           client.get_employees(),
           client.get_payroll_list(3, 2026)
       )
   ```

3. **Token Management:**
   ```python
   # Save token for reuse
   client.login('admin', 'admin123')
   with open('config.json', 'w') as f:
       json.dump({'token': client.token}, f)
   
   # Load token for next run
   with open('config.json', 'r') as f:
       config = json.load(f)
       client.token = config['token']
   ```

4. **Error Retry Logic:**
   ```python
   import time
   
   def retry_request(func, max_retries=3):
       for attempt in range(max_retries):
           try:
               return func()
           except Exception as e:
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)  # Exponential backoff
               else:
                   raise e
   
   # Usage
   data = retry_request(lambda: client.get_employees())
   ```

---

## 📞 Common Issues - Python

| Issue | Solution |
|-------|----------|
| `ConnectionError: Cannot connect` | Check if Flask backend is running: `python wsgi.py` |
| `401 Unauthorized` | Token hết hạn → Login lại |
| `FileNotFoundError: token.txt` | Chưa login → Call `client.login()` trước |
| `json.JSONDecodeError` | Response không phải JSON → Check API server logs |
| `SSL Error` | Backend dùng HTTPS → Update URL trong config |

---

**Ready to build Python frontend!** 🎉
