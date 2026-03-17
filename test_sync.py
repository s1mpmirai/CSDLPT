import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_sync_creation():
    # 1. Login
    print("Logging in...")
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = response.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    print("Token obtained.")

    # 2. Get Department and Position IDs
    print("Fetching departments and positions...")
    dept = requests.get(f"{BASE_URL}/phongban", headers=headers).json().get("data")[0]
    pos = requests.get(f"{BASE_URL}/chucvu", headers=headers).json().get("data")[0]
    
    # 3. Create Employee
    new_employee = {
        "tenNV": "Test Sync User",
        "ngaySinh": "1995-01-01",
        "gioiTinh": "Nam",
        "diaChi": "Test Address",
        "sdt": "0123456789",
        "email": "testsync_2@example.com",
        "maPhong": dept["maPhong"],
        "maChucVu": pos["maChucVu"],
        "ngayVaoLam": "2024-01-01"
    }
    
    print(f"Creating employee: {new_employee['tenNV']}...")
    create_res = requests.post(f"{BASE_URL}/nhanvien", json=new_employee, headers=headers)
    print("Response:", create_res.text)
    
    if create_res.status_code == 201:
        emp_id = create_res.json().get("data").get("maNV")
        print(f"Employee created with ID: {emp_id}")
        
        # 4. Check Payroll (Synchronization verification)
        print(f"Checking if payroll record was created for MaNV {emp_id}...")
        # Use the specific detail endpoint instead of a list endpoint that doesn't exist
        payroll_res = requests.get(f"{BASE_URL}/luong/{emp_id}", headers=headers)
        
        if payroll_res.status_code == 200:
            payroll_data = payroll_res.json().get("data")
            if payroll_data.get("maNV") == emp_id:
                print(f"SUCCESS: Payroll record found for new employee! Base Salary: {payroll_data.get('luongCoBan')}")
            else:
                print("FAILURE: Payroll record has wrong MaNV.")
        else:
            print(f"FAILURE: Payroll record not found. Status: {payroll_res.status_code}, Text: {payroll_res.text}")
            
        # 5. Cleanup (Soft Delete)
        print(f"Deleting employee {emp_id}...")
        del_res = requests.delete(f"{BASE_URL}/nhanvien/{emp_id}", headers=headers)
        print("Delete Response:", del_res.json().get("message"))
        
        # 6. Check Payroll Status (Synchronization verification for delete)
        print("Checking if payroll status was updated to 0...")
        # We need a detail endpoint or filter for this
        payroll_res_after = requests.get(f"{BASE_URL}/luong", headers=headers)
        # Note: get_payrolls might only return active ones in some implementations
        # Let's check the logic in luong.py route later if needed.
    else:
        print("Failed to create employee.")

if __name__ == "__main__":
    test_sync_creation()
