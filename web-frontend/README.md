# HR PAYROLL WEB FRONTEND

Web-based frontend cho hệ thống quản lý lương nhân sự. Giao diện đơn giản, nhẹ nhàng và dễ chỉnh sửa.

## 📋 Yêu cầu

- **Backend**: Flask API chạy trên `http://localhost:5000`
- **Database**: MySQL (DB1_NHANSU, DB2_LUONG)
- **Browser**: Chrome, Firefox, Edge, Safari (hiện đại)

## 🚀 Cách sử dụng

### 1. **Chuẩn bị Backend**

Chắc chắn Flask backend đang chạy:

```bash
cd backend
python app.py
```

Hoặc nếu dùng terminal khác:
```bash
python run_flask_server.py
```

Backend phải chạy trên `http://localhost:5000`

### 2. **Mở Web Frontend**

Cách 1: **Mở trực tiếp file HTML** (Đơn giản nhất)
- Click đúp `index.html` hoặc drag vào browser
- Hoặc: `File → Open File` rồi chọn `index.html`

Cách 2: **Dùng Python HTTP Server** (Khuyên dùng)
```bash
cd web-frontend

# Python 3
python -m http.server 8000

# Hoặc Python 2 (nếu cần)
python -m SimpleHTTPServer 8000
```

Sau đó mở browser: `http://localhost:8000`

Cách 3: **Dùng Live Server** (Với VS Code)
- Cài extension: "Live Server" từ ritwickdey
- Click chuột phải `index.html` → "Open with Live Server"

### 3. **Đăng nhập**

Sử dụng credential từ backend:

| Tài khoản | Mật khẩu | Vai trò |
|-----------|----------|--------|
| admin     | admin123 | Admin  |
| ketoan    | ketoan123 | Kế toán |
| nhanvien  | nhanvien123 | Nhân viên |

## 📁 Cấu trúc Thư mục

```
web-frontend/
├── index.html          # Login page
├── dashboard.html      # Dashboard page
├── css/
│   └── style.css       # Styling cho toàn bộ app
├── js/
│   ├── api-client.js   # API communication layer
│   ├── login.js        # Login page logic
│   └── dashboard.js    # Dashboard page logic
└── assets/             # Folder cho hình ảnh/fonts (để sau)
```

## 🎨 Features Hiện tại

### ✅ Hoàn thành
- [x] **Login Page** - Đăng nhập với 3 role khác nhau
- [x] **Dashboard** - Giao diện chính với menu role-based
- [x] **Statistics** - Hiển thị thống kê nhân viên, lương
- [x] **Employee List** - Danh sách nhân viên
- [x] **Payroll List** - Danh sách tính lương
- [x] **Department List** - Danh sách phòng ban
- [x] **Reports** - Báo cáo lương

### 🔄 Đang phát triển
- [ ] Thêm/sửa/xóa nhân viên (forms)
- [ ] Thêm/sửa/xóa phòng ban (forms)
- [ ] Tính lương tự động
- [ ] Xuất Excel báo cáo
- [ ] User profile settings
- [ ] Chỉnh mật khẩu

### 📅 Tính năng sau
- [ ] Import từ Excel
- [ ] Notifications/Alerts
- [ ] Mobile app (React Native/Flutter)
- [ ] Single Sign-On (SSO)
- [ ] Advanced Reports & Analytics

## 🔧 Chỉnh sửa & Tùy biến

### Thay đổi API Base URL

Mở `js/api-client.js`, tìm dòng:
```javascript
constructor(baseUrl = 'http://localhost:5000')
```

Thay đổi URL nếu backend chạy ở chỗ khác.

### Thay đổi Màu sắc

Mở `css/style.css`, tìm phần `:root`:
```css
:root {
    --color-primary: #4a99ff;
    --color-bg-dark: #0d0d0d;
    /* ... */
}
```

Thay đổi giá trị hex color theo ý muốn.

### Thêm Menu Item Mới

Mở `js/dashboard.js`, tìm `roleMenuConfig`:
```javascript
const roleMenuConfig = {
    admin: [
        { id: 'home', label: 'Trang chủ', icon: '🏠' },
        // Thêm item mới ở đây
        { id: 'newpage', label: 'Trang mới', icon: '⭐' },
    ],
    // ...
};
```

### Thêm Trang Mới

1. Tạo section mới trong `dashboard.html`:
```html
<div id="newpageSection" class="content-section" style="display: none;">
    <h2>Trang mới</h2>
    <!-- Content -->
</div>
```

2. Thêm function trong `js/dashboard.js`:
```javascript
async function loadNewPage() {
    // Load data
}
```

3. Thêm call vào `showSection()`:
```javascript
if (sectionId === 'newpage') loadNewPage();
```

## 🐛 Troubleshooting

### "Failed to establish connection"
- Kiểm tra backend có đang chạy không: `http://localhost:5000`
- Kiểm tra firewall có chặn port 5000 không
- Chạy backend: `python app.py`

### "CORS Error"
- Hiện tại Flask backend chưa cấu hình CORS
- Cần thêm vào backend:
```python
from flask_cors import CORS
CORS(app)
```

### Login không hoạt động
- Kiểm tra credentials có đúng không
- Kiểm tra console (F12 → Console) có lỗi gì không
- Thử refresh page (Ctrl+F5)

### Data không hiển thị
- Kiểm ra network tab (F12 → Network) có request nào bị lỗi không
- Kiểm tra backend API response có đúng format không

## 📚 API Endpoints (Reference)

Tất cả endpoints đều require Bearer token trong header:
```
Authorization: Bearer <token>
```

### Authentication
- `POST /api/auth/login` - Đăng nhập

### Employees
- `GET /api/employees` - Danh sách nhân viên
- `GET /api/employees/{id}` - Chi tiết
- `POST /api/employees` - Tạo mới
- `PUT /api/employees/{id}` - Cập nhật
- `DELETE /api/employees/{id}` - Xóa

### Payrolls
- `GET /api/payrolls` - Danh sách lương
- `POST /api/payrolls/calculate` - Tính lương
- `PUT /api/payrolls/{id}` - Cập nhật

### Departments
- `GET /api/departments` - Danh sách phòng ban
- `POST /api/departments` - Tạo mới
- `PUT /api/departments/{id}` - Cập nhật
- `DELETE /api/departments/{id}` - Xóa

## 💡 Tips

1. **Mở DevTools**: F12 hoặc Ctrl+Shift+I
2. **Console**: Xem logs và errors
3. **Network Tab**: Inspect API calls
4. **Local Storage**: Xem saved token & user (Application tab)
5. **Responsive Mode**: Ctrl+Shift+M để test mobile view

## 📝 Development Notes

### Cấu trúc Project
- Lightweight: Không cần build process hoặc bundler
- Vanilla JavaScript: Dễ hiểu, dễ sửa
- CSS Variables: Dễ thay đổi theme
- Modular JS: Chia tách logic rõ ràng

### Cải thiện trong tương lai
- [ ] Thêm input validation
- [ ] Add form builders
- [ ] Implement caching
- [ ] Add offline support
- [ ] PWA support

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra console (F12)
2. Kiểm tra network tab
3. Xem lại credential
4. Chạy lại backend

---

**Last Updated**: March 17, 2026  
**Version**: 1.0.0
