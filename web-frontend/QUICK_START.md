# 🚀 QUICK START - HR PAYROLL WEB FRONTEND

## 5 Bước để chạy Web Frontend

### 1️⃣ Khởi động Flask Backend

Mở terminal/PowerShell:

```bash
cd d:\DATA\Code\CSDLPT\backend
python app.py
```

Chờ tới khi thấy:
```
* Running on http://127.0.0.1:5000
```

**Để nguyên terminal này chạy** (đừng đóng)

### 2️⃣ Khởi động Web Server

**Cách A: Click file** (Đơn giản nhất)
- Tìm file `START_SERVER.bat` trong `web-frontend/`
- Click đúp vào nó
- Browser sẽ tự mở `http://localhost:8000`

**Cách B: Mở terminal mới** (Nếu batch file không chạy)
```bash
cd d:\DATA\Code\CSDLPT\web-frontend
python -m http.server 8000
```

Chờ tới khi thấy:
```
Serving HTTP on 0.0.0.0 port 8000
```

### 3️⃣ Mở Browser

Nếu chưa mở, hãy mở:
```
http://localhost:8000
```

Hoặc click vào link:
👉 [http://localhost:8000](http://localhost:8000)

### 4️⃣ Đăng nhập

Dùng một trong các tài khoản:

```
Tài khoản: admin      | Mật khẩu: admin123
Tài khoản: ketoan     | Mật khẩu: ketoan123  
Tài khoản: nhanvien   | Mật khẩu: nhanvien123
```

### 5️⃣ Thưởng thức! 🎉

Bạn đã vào Dashboard!

---

## 📋 Checklist Trước Khi Chạy

- [ ] Cài Python 3.8+
- [ ] Cài MySQL
- [ ] Backend databases đã import
- [ ] Backend chạy ở `http://localhost:5000`
- [ ] Không có port conflicts

## 🛑 Nếu Có Lỗi

### Error: "Failed to establish connection"
```
❌ Kiểm tra: Backend có đang chạy không?
✅ Giải pháp: Chạy `python app.py` ở terminal backend
```

### Error: "Tên đăng nhập hoặc mật khẩu không đúng"
```
❌ Kiểm tra: Credential có đúng không?
✅ Giải pháp: Dùng tài khoản: admin / admin123
```

### Browser mở trang trắng
```
❌ Kiểm tra: Web server có chạy không?
✅ Giải pháp: Chuyển sang tab terminal, vào cd web-frontend, chạy: python -m http.server 8000
```

### Port 8000 đã được sử dụng
```
❌ Kiểm tra: Có app khác dùng port 8000 không?
✅ Giải pháp: Chạy server ở port khác:
   python -m http.server 9000
   Rồi mở: http://localhost:9000
```

## 🔧 Tùy Chỉnh Nhanh

### Thay Backend URL

Mở `js/api-client.js` dòng ~15:

**Trước:**
```javascript
constructor(baseUrl = 'http://localhost:5000')
```

**Sau:** (Nếu backend ở chỗ khác)
```javascript
constructor(baseUrl = 'http://192.168.1.100:5000')  // Tùy chỉnh IP/port
```

### Thay Port Web Server

```bash
# Từ 8000 sang 3000
python -m http.server 3000

# Từ 8000 sang 5173
python -m http.server 5173
```

## 📂 File Quan Trọng

```
web-frontend/
├── index.html          ← Login page
├── dashboard.html      ← Main page
├── START_SERVER.bat    ← Click để chạy
├── css/style.css       ← Edit màu ở đây
├── js/api-client.js    ← Edit backend URL ở đây
└── js/dashboard.js     ← Edit menu/logic ở đây
```

## 💾 Lưu Dữ Liệu

- Token được lưu trong **Local Storage** của browser
- Tự động gửi kèm mỗi API request
- Session hết khi refresh page (nếu frontend bị reload)

## 📊 Theo Dõi Network

Mở **DevTools** (F12):

1. Chuyển sang tab **Network**
2. Làm các action (login, load data, etc)
3. Xem API requests/responses
4. Kiểm tra status code (200 = OK, 401 = Lỗi xác thực)

## 🎯 Tiếp Theo

- [ ] Tùy chỉnh giao diện (CSS)
- [ ] Thêm forms (add/edit employees)
- [ ] Kết nối database views
- [ ] Deploy lên server
- [ ] Tối ưu performance

---

**Happy Coding! 🚀**

Mọi câu hỏi hãy tham khảo file `README.md`
