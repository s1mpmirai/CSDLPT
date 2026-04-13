---
name: csdlpt-distributed-db-flow
description: "Use when analyzing, onboarding, debugging, or extending the CSDLPT HR payroll system with vertically partitioned MySQL databases DB1_NHANSU and DB2_LUONG. Covers end-to-end web flow, API contracts, cross-database joins, sync rules, and role-based data access."
argument-hint: "Task: onboarding | debug-web-no-data | api-contract-check | db-sync-check | sql-focus-review"
---

# CSDLPT Distributed DB Flow Skill

## What This Skill Produces
- A compact, evidence-based map of the full system flow: web frontend -> Flask API -> DB1_NHANSU + DB2_LUONG.
- A SQL-first verification checklist for distributed payroll workloads.
- A mismatch checklist to quickly diagnose "web has no data" and API contract drift.

## Project Topology (Authoritative Files)
- Backend app factory and wiring:
  - backend/app/__init__.py
  - backend/config.py
  - backend/wsgi.py
- Core HR models (DB1):
  - backend/app/models/nhanvien.py
- Core Payroll models (DB2):
  - backend/app/models/luong.py
- API routes:
  - backend/app/routes/auth.py
  - backend/app/routes/nhanvien.py
  - backend/app/routes/luong.py
  - backend/app/routes/phongban.py
  - backend/app/routes/chucvu.py
  - backend/app/routes/compat.py
  - backend/app/routes/seed.py
- Frontend entrypoints:
  - web-frontend/index.html
  - web-frontend/dashboard.html
  - web-frontend/js/login.js
  - web-frontend/js/dashboard.js
  - web-frontend/js/api-client.js
  - web-frontend/js/config.js
- SQL definitions (highest priority for distributed DB):
  - backend/sql/DB1_NhanSu.sql
  - backend/sql/DB2_Luong.sql
  - backend/sql/docker_init.sql

## System Architecture Summary
- Partition strategy: vertical split by business domain.
  - DB1_NHANSU: organizational + employee profile data.
  - DB2_LUONG: salary master, monthly payroll details, insurance configs, salary history.
- Flask SQLAlchemy binds:
  - db1_nhansu -> DB1_NHANSU
  - db2_luong -> DB2_LUONG
- Cross-DB transparency:
  - DB1 view vw_AdminNhanVienDayDu joins DB1 tables with DB2_LUONG.BangLuong.
  - API-level transparency also exists in routes that merge DB2 salary rows with DB1 employee names.

## End-to-End Runtime Flows

### 1) Authentication Flow
1. Frontend login form submits username/password/role.
2. POST /api/auth/login validates hardcoded account map.
3. JWT token issued with claims (role, and maNV for nhanvien account).
4. Frontend stores token in localStorage and uses Bearer token on all API calls.

### 2) Dashboard Stats Flow
1. Dashboard boot calls GET /api/statistics.
2. compat route computes:
   - total_employees from DB1 NhanVien (TrangThai=1)
   - total_departments from DB1 PhongBan
   - total_payroll from DB2 ChiTietLuongThang
3. For nhanvien role, route scopes payroll to claim maNV.

### 3) Employee Management Sync Flow (Distributed Integrity)
1. Admin creates employee via POST /api/nhanvien.
2. Backend inserts NhanVien in DB1.
3. Same transaction also creates default BangLuong in DB2.
4. Commit completes only after both sides are staged.
5. On soft delete (DELETE /api/nhanvien/<id>):
   - DB1 NhanVien.TrangThai -> 0
   - DB2 BangLuong.TrangThai -> 0

### 4) Monthly Payroll Display Flow
1. UI requests GET /api/luong/danh-sach?thang=<m>&nam=<y>.
2. DB2 query returns ChiTietLuongThang for month/year.
3. API gathers MaNV list and fetches DB1 names.
4. API returns unified payload with payroll + employee identity.

### 5) Department and Position Flow
- Departments: /api/phongban (DB1 PhongBan)
- Positions: /api/chucvu (DB1 ChucVu)

## SQL-Focused Distributed Review (DB1 + DB2)

### DB1_NHANSU (backend/sql/DB1_NhanSu.sql)
- Tables:
  - PhongBan
  - ChucVu
  - NhanVien (FK to PhongBan, ChucVu)
- Indexes: email, department, position, status.
- Views:
  - vw_NhanVienDayDu
  - vw_AdminNhanVienDayDu (cross-db join to DB2_LUONG.BangLuong)
  - vw_NhanVienTheoPhongBan
- Procedures:
  - sp_ThemNhanVien
  - sp_CapNhatNhanVien
  - sp_XoaNhanVien
- Security grants for user_nhanvien and user_ketoan included.

### DB2_LUONG (backend/sql/DB2_Luong.sql)
- Tables:
  - BangLuong
  - ChiTietLuongThang (with generated LuongThucLinh)
  - BaoHiemConfig
  - LichSuThayDoiLuong
  - HopDongLuong
- Views:
  - vw_LuongThangChiTiet
  - vw_TongHopLuongThang
- Procedures:
  - sp_CapNhatBangLuong
  - sp_TinhLuongThang
  - sp_TinhLuongToanBoThang
- Unique constraints and indexes support monthly uniqueness and lookup speed.

## Critical Invariants (Must Hold)
- Every active NhanVien that participates in payroll must have one active BangLuong row.
- ChiTietLuongThang uniqueness on (MaNV, Thang, Nam) must not be violated.
- Role nhanvien can only view own payroll rows.
- API response shapes must match frontend expectations per screen.

## Known Drift and Risk Hotspots
- Documentation drift exists: some docs mention /api/employees or /api/payrolls, while runtime routes use /api/nhanvien and /api/luong (compat aliases partially bridge this).
- Frontend rendering expects different payload shapes across sections; verify each table renderer against actual response schema.
- The DB1 script contains grants and references DB2 procedure execution; ensure execution order and MySQL privileges are consistent in local setup.
- docker_init.sql correctly runs DB2 first, then DB1, to support cross-db references.

## Debug Workflow: "Web Connected But No Data"
1. Verify backend and frontend servers are both running.
2. Verify login works and token is stored in localStorage.
3. Verify API directly with token:
   - /api/statistics
   - /api/nhanvien
   - /api/luong/danh-sach?thang=<m>&nam=<y>
4. Verify DB row presence in both DBs (queries below).
5. Verify response contract matches table mapping in dashboard.js.
6. Verify role restrictions are not hiding data unexpectedly.

## SQL Verification Snippets (Run Manually)
```sql
-- DB1 checks
USE DB1_NHANSU;
SELECT COUNT(*) AS active_employees FROM NhanVien WHERE TrangThai = 1;
SELECT MaNV, TenNV, MaPhong, MaChucVu, TrangThai FROM NhanVien ORDER BY MaNV;
SELECT * FROM vw_NhanVienTheoPhongBan;

-- Cross-db transparency check (from DB1)
SELECT * FROM vw_AdminNhanVienDayDu LIMIT 20;

-- DB2 checks
USE DB2_LUONG;
SELECT COUNT(*) AS active_salary_profiles FROM BangLuong WHERE TrangThai = 1;
SELECT MaNV, Thang, Nam, LuongThucLinh, TrangThai
FROM ChiTietLuongThang
ORDER BY Nam DESC, Thang DESC, MaNV;

-- Integrity check: employees without salary profile
SELECT nv.MaNV, nv.TenNV
FROM DB1_NHANSU.NhanVien nv
LEFT JOIN DB2_LUONG.BangLuong bl ON nv.MaNV = bl.MaNV
WHERE nv.TrangThai = 1 AND bl.MaNV IS NULL;
```

## Output Template For Future Use
### Scope
- Task:
- Environment:
- Role tested:

### Flow Findings
- Startup and config:
- Auth and token:
- API contracts:
- DB1/DB2 data state:
- Cross-db transparency:
- Sync integrity:

### Risks and Fix Order
1. Critical:
2. Major:
3. Minor:

### Validation
- API checks passed:
- SQL checks passed:
- UI sections confirmed:
