from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.nhanvien import NhanVien, PhongBan
from app.models.luong import ChiTietLuongThang

compat_bp = Blueprint('compat', __name__)

@compat_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """Return basic counts for frontend usage."""
    try:
        total_employees = NhanVien.query.filter_by(TrangThai=1).count()
        total_departments = PhongBan.query.count()

        # Total payroll for current month (sum of net salary)
        from datetime import datetime
        now = datetime.now()
        month = request.args.get('month', f"{now.year}-{now.month:02d}")
        year, month_num = month.split('-') if '-' in month else (str(now.year), str(now.month))
        try:
            year = int(year)
            month_num = int(month_num)
        except ValueError:
            year = now.year
            month_num = now.month

        from flask_jwt_extended import get_jwt
        claims = get_jwt()
        user_role = claims.get('role')
        user_ma_nv = claims.get('maNV')

        if user_role == 'nhanvien':
            # Chỉ tính lương của chính họ
            payrolls = ChiTietLuongThang.query.filter_by(MaNV=user_ma_nv, Thang=month_num, Nam=year).all()
            total_payroll = sum(p.calculate_luong_thuc_linh() for p in payrolls) if payrolls else 0
            
            return jsonify({
                'success': True,
                'data': {
                    'total_employees': 1,
                    'total_departments': 1,
                    'total_payroll': float(total_payroll),
                }
            }), 200

        payrolls = ChiTietLuongThang.query.filter_by(Thang=month_num, Nam=year).all()
        total_payroll = sum(p.calculate_luong_thuc_linh() for p in payrolls) if payrolls else 0

        return jsonify({
            'success': True,
            'data': {
                'total_employees': total_employees,
                'total_departments': total_departments,
                'total_payroll': float(total_payroll),
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@compat_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    """List employees (pagination and filtering compatible with frontend)."""
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        
        # Support both 'phong_ban' and 'phongBan' due to potential frontend inconsistencies
        phong_ban_id = request.args.get('phong_ban', type=int)
        if phong_ban_id is None:
            phong_ban_id = request.args.get('phongBan', type=int)

        query = NhanVien.query.filter_by(TrangThai=1)
        
        if phong_ban_id:
            query = query.filter_by(MaPhong=phong_ban_id)
            
        paginated = query.paginate(page=page, per_page=page_size)

        data = [
            {
                'employee_id': nv.MaNV,
                'first_name': nv.TenNV,
                'last_name': '',
                'email': nv.Email,
                'position_name': nv.chucvu.TenChucVu if nv.chucvu else None,
                'department_name': nv.phongban.TenPhong if nv.phongban else None,
            }
            for nv in paginated.items
        ]

        return jsonify({
            'success': True,
            'data': {
                'items': data,
                'total': paginated.total,
                'page': paginated.page,
                'pages': paginated.pages,
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@compat_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    """List departments with employee counts."""
    try:
        depts = PhongBan.query.all()
        data = [
            {
                'department_id': d.MaPhong,
                'name': d.TenPhong,
                'employee_count': NhanVien.query.filter_by(MaPhong=d.MaPhong, TrangThai=1).count(),
            }
            for d in depts
        ]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@compat_bp.route('/payrolls', methods=['GET'])
@jwt_required()
def get_payrolls():
    """List payrolls for a given month."""
    try:
        month = request.args.get('month')
        if not month:
            from datetime import datetime
            now = datetime.now()
            month = f"{now.year}-{now.month:02d}"

        if '-' in month:
            year, month_num = month.split('-')
        else:
            # Fallback for unexpected format
            year = month[:4]
            month_num = month[4:]
            
        year = int(year)
        month_num = int(month_num)

        payrolls = ChiTietLuongThang.query.filter_by(Thang=month_num, Nam=year).all()

        items = []
        for p in payrolls:
            employee = NhanVien.query.get(p.MaNV)
            items.append({
                'payroll_id': p.MaChiTiet,
                'employee_name': employee.TenNV if employee else f'NV {p.MaNV}',
                'month': f"{year}-{month_num:02d}",
                'base_salary': float(p.LuongCoBan),
                'bonus': float(p.Thuong or 0),
                'net_salary': float(p.calculate_luong_thuc_linh()),
            })

        return jsonify({
            'success': True,
            'data': {
                'items': items,
                'total': len(items),
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@compat_bp.route('/reports/payroll', methods=['GET'])
@jwt_required()
def get_report_payroll():
    """Report API alias for statistics."""
    return get_statistics()

@compat_bp.route('/verify-view', methods=['GET'])
@jwt_required()
def verify_view():
    """Verify the cross-DB view vw_AdminNhanVienDayDu."""
    try:
        from app import db
        result = db.session.execute(db.text("SELECT * FROM vw_AdminNhanVienDayDu LIMIT 5"))
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in result]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
