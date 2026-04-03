# Báo Cáo Triển Khai Đồ Án: Phân Mảnh Cơ Sở Dữ Liệu Lương & Nhân Sự

Tài liệu này tổng hợp lại cách dự án thực tế triển khai các yêu cầu bài toán liên quan đến Phân mảnh cơ sở dữ liệu, đảm bảo Tính trong suốt, Đồng bộ thao tác, và Phân quyền bảo mật như được yêu cầu. Các thành viên trong nhóm có thể sử dụng tài liệu này để làm cơ sở viết báo cáo (Word/Slide).

---

## 1. Phân mảnh dọc & Thiết kế 2 CSDL vật lý (Yêu cầu 1)

Thay vì chạy trên một CSDL duy nhất gây rủi ro lộ thông tin nhạy cảm (Lương thưởng), hệ thống áp dụng kỹ thuật **Phân mảnh dọc** ở cấp độ ứng dụng bằng cách chia thành 2 DB riêng biệt:

- **`db1_nhansu`**: Chứa thông tin public (Nhân viên, Phòng ban, Chức vụ...).
- **`db2_luong`**: Chứa thông tin private, nhạy cảm (Bảng lương, Cấu hình bảo hiểm, Chi tiết lương...).

**Cách Code thực hiện:**
Trong Flask Backend, `SQLAlchemy Binds` được sử dụng để kết nối đồng thời với cả 2 DB (file `config.py`):
```python
SQLALCHEMY_BINDS = {
    'db1_nhansu': 'mysql+pymysql://.../DB1_NHANSU',
    'db2_luong': 'mysql+pymysql://.../DB2_LUONG'
}
```
Các Model khai báo rõ ràng vị trí lưu trữ của mình thông qua biến `__bind_key__`.
- File `models/nhanvien.py`: Class `NhanVien` chỉ định `__bind_key__ = 'db1_nhansu'`.
- File `models/luong.py`: Class `BangLuong` chỉ định `__bind_key__ = 'db2_luong'`.

Điều này tách biệt hoàn toàn 2 CSDL về mặt vật lý nhưng ứng dụng vẫn có thể trỏ đến để thao tác.

## 2. Tính trong suốt (Yêu cầu 2)

Thay vì tạo `View` hoặc `Stored Procedure` thông qua Linked Server ở tầng Database, dự án này đảm bảo **Tính trong suốt (Transparency) ở tầng API / Backend Application**. Giao diện/Admin khi sử dụng chỉ thấy một tập dữ liệu như đang làm việc trên 1 bảng duy nhất.

**Cách Code thực hiện:**
Khi Frontend muốn hiển thị DB Lương cùng Tên Nhân viên, Back-end sẽ tự động làm thao tác JOIN trên bộ nhớ đệm (thể hiện ở API `GET /api/luong/danh-sach` trong file `routes/luong.py`):
1. Query mọi hóa đơn lương từ `db2_luong`.
2. Bóc tách ra danh sách `MaNV`.
3. Query sang `db1_nhansu` để lấy tên của nhân viên (`TenNV`) tương ứng.
4. Gộp lại và gửi ra dưới dạng 1 JSON Object hợp nhất duy nhất cho Frontend.

Admin hoặc Frontend khi request không cần phải quan tâm làm thế nào để gọi 2 nơi, mà Backend đã "che đi" việc phân tán và đảm bảo tính trong suốt cho người dùng cuối.

## 3. Yêu cầu Đồng bộ thao tác (Yêu cầu 3)

Hệ thống cần tránh tình trạng Nhân viên có bên DB1 nhưng bị sót lương bên DB2. Mã nguồn đảm bảo điều này bằng việc tự động hóa thao tác sang 2 CSDL khi thêm hoặc xóa nhân viên.

**Cách Code thực hiện:**
- **Khi Insert (Thêm mới NV)**: Ở API route `POST /api/nhanvien`, sau khi lưu vào `NhanVien` của DB1 thành công, hệ thống tiếp tục khởi tạo một bản ghi `BangLuong` mặc định lưu sang DB2. Sau đó mới gọi `db.session.commit()`.
- **Khi Delete (Xoá NV - Soft delete)**: Ở API route `DELETE /api/nhanvien/<maNV>`, thay vì xóa hẳn, code đánh dấu `TrangThai = 0` (Nghỉ việc) ở DB1. Đồng thời tìm kiếm thông tin bảng lương của `MaNV` này ở DB2 để cập nhật `TrangThai = 0`. Mọi thứ gói gọn trong một đơn vị giao dịch. Nếu bên DB2 lỗi sẽ rollback luôn DB1, đảm bảo tính toàn vẹn dư liệu.

## 4. Cơ chế Phân quyền bảo mật (Yêu cầu 4)

Bảo mật được quản lý bằng JWT (JSON Web Tokens) với Role kiểm tra trên từng API. Điều này đảm bảo ai có quyền nào thì chỉ được thao tác module đó, phòng chống trường hợp nhân sự IT lấy quyền Admin để trích xuất DB2 khi không có quyền.

**Cách Code thực hiện:**
- Code sử dụng hàm giả lập `check_permission(...)`.
- Group API Nhân sự (Quản lý NV): Chỉ Role `admin` mới được thêm, cập nhật, xóa thông qua `check_permission('admin')`.
- Group API Lương: Chỉ Role `ketoan` hoặc `admin` được chỉ định (hoặc cấp quyền đặc biệt) mới được duyệt các API như `GET /api/luong` bằng `check_permission('admin_ketoan')`.
- Đặc biệt, bản thân **Role Nhân Viên** chỉ có thể xem được dữ liệu lương của **chính mình**: Ở API `GET /api/luong/chi-tiet/id/<id>`, hệ thống đối chiếu `maNV` trên JWT token. Nếu user xem lương của 1 `maNV` khác -> `Return 403 bạn không có quyền xem lương của người khác`.

## 5. Đề xuất kịch bản Test case để báo cáo (Yêu cầu 5)

Thành viên nhóm có thể liệt kê các Test case sau vào báo cáo để chứng minh đồ án đáp ứng tiêu chí điểm tuyệt đối:

### TC1. Tính đúng đắn cơ chế Đồng bộ (Thêm NV)
- **Hành động**: Admin tạo mới 1 nhân viên A (Mã 99) qua trình quản lý.
- **Kỳ vọng**: Mở MySQL Workbench, xem database `db1_nhansu` thấy xuất hiện nhân viên 99. Đồng thời mở database `db2_luong` cũng thấy một "Bảng lương" phát sinh cho Nhân viên mã 99.

### TC2. Tính đúng đắn cơ chế Đồng bộ (Xóa/Nghỉ việc NV)
- **Hành động**: Gọi hàm Xóa hoặc Đuổi việc nhân viên 99.
- **Kỳ vọng**: Trường `TrangThai` ở cả 2 bảng (DB1, DB2) của nhân viên 99 đồng thời về `0`.

### TC3. Tính trong suốt của Admin
- **Hành động**: Gọi API Danh sách lương `GET /api/luong/danh-sach`.
- **Kỳ vọng**: Danh sách JSON trả về đầy đủ tiền lương (DB2) kẹp chung với tên, email nhân viên (từ DB1) trong 1 lần hiển thị.

### TC4. Phân Quyền Bảo Mật
- **Phân quyền Kế toán**: Kế toán đăng nhập, truy cập `/api/nhanvien` bằng hàm xóa -> API trả lỗi Forbidden do thiếu role admin.
- **Phân quyền Nhân viên**: Nhân viên (Mã NV: 20) đăng nhập. Gọi `/api/luong/chi-tiet/id/50` (Giả sử 50 là lương của bạn giám đốc) -> Kết quả: API từ chối hiển thị và trả về lỗi không có quyền truy cập. Gọi đúng mã 20 -> Hệ thống trả về cấu trúc lương chính xác hiển thị lên frontend.
