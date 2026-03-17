from app import create_app, db
import sys

def create_view():
    try:
        app = create_app()
        with app.app_context():
            # Create view in DB1 (default) that joins with DB2_LUONG
            db.session.execute(db.text("""
                CREATE OR REPLACE VIEW vw_AdminNhanVienDayDu AS
                SELECT 
                    nv.MaNV,
                    nv.TenNV,
                    pb.TenPhong,
                    cv.TenChucVu,
                    l.LuongCoBan,
                    l.HeSoLuong,
                    l.PhuCapChucVu,
                    l.PhuCapPhongBan,
                    (l.LuongCoBan * l.HeSoLuong + l.PhuCapChucVu + l.PhuCapPhongBan) AS TongThuNhap
                FROM NhanVien nv
                INNER JOIN PhongBan pb ON nv.MaPhong = pb.MaPhong
                INNER JOIN ChucVu cv ON nv.MaChucVu = cv.MaChucVu
                LEFT JOIN DB2_LUONG.BangLuong l ON nv.MaNV = l.MaNV
            """))
            db.session.commit()
            print("View 'vw_AdminNhanVienDayDu' created successfully.")
    except Exception as e:
        print(f"Error creating view: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_view()
