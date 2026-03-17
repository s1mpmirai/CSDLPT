/**
 * Dashboard Page JavaScript
 */

let currentSection = 'home';
let currentEmployeePage = 1;
let currentEmployeeSearch = '';
let currentPayrollSearch = '';

const roleMenuConfig = {
    admin: [
        { id: 'home', label: 'Trang chủ', icon: '🏠' },
        { id: 'employees', label: 'Nhân viên', icon: '👥' },
        { id: 'payroll', label: 'Quản lý lương', icon: '💰' },
        { id: 'departments', label: 'Phòng ban', icon: '🏢' },
        { id: 'reports', label: 'Báo cáo', icon: '📊' },
    ],
    ketoan: [
        { id: 'home', label: 'Trang chủ', icon: '🏠' },
        { id: 'payroll', label: 'Quản lý lương', icon: '💰' },
        { id: 'reports', label: 'Báo cáo', icon: '📊' },
    ],
    nhanvien: [
        { id: 'home', label: 'Trang chủ', icon: '🏠' },
        { id: 'payroll', label: 'Lương của tôi', icon: '💰' },
    ],
};

document.addEventListener('DOMContentLoaded', async function() {
    // Check if user is logged in
    const userKey = CONFIG?.ADVANCED?.USER_KEY || 'user';
    const tokenKey = CONFIG?.ADVANCED?.TOKEN_KEY || 'token';
    
    const user = JSON.parse(localStorage.getItem(userKey) || 'null');
    const token = localStorage.getItem(tokenKey);
    
    if (!user || !token) {
        window.location.href = 'index.html';
        return;
    }
    
    // Set user info
    const userNameEl = document.getElementById('userName');
    if (userNameEl) userNameEl.textContent = user.username;
    
    const userRoleEl = document.getElementById('userRole');
    if (userRoleEl) userRoleEl.textContent = getRoleName(user.role);
    
    const welcomeNameEl = document.getElementById('welcomeName');
    if (welcomeNameEl) welcomeNameEl.textContent = user.username;
    
    // Build menu based on role
    buildMenu(user.role);
    
    // Setup logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) logoutBtn.addEventListener('click', logout);

    const payrollMonth = document.getElementById('payrollMonth');
    if (payrollMonth) {
        payrollMonth.addEventListener('change', loadPayrolls);
    }

    // Setup payroll search
    const payrollSearch = document.getElementById('payrollSearch');
    const payrollSearchBtn = document.getElementById('payrollSearchBtn');
    
    if (payrollSearch) {
        payrollSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                currentPayrollSearch = payrollSearch.value;
                loadPayrolls();
            }
        });
    }

    if (payrollSearchBtn) {
        payrollSearchBtn.addEventListener('click', function() {
            currentPayrollSearch = payrollSearch.value;
            loadPayrolls();
        });
    }
    
    // Setup search
    const employeeSearch = document.getElementById('employeeSearch');
    const searchBtn = document.getElementById('searchBtn');
    
    if (employeeSearch) {
        employeeSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                currentEmployeeSearch = employeeSearch.value;
                currentEmployeePage = 1;
                loadEmployees();
            }
        });
    }

    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            currentEmployeeSearch = employeeSearch.value;
            currentEmployeePage = 1;
            loadEmployees();
        });
    }
    
    // Load data
    await loadStatistics();
});

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

/**
 * Get role display name
 */
function getRoleName(role) {
    const roleNames = {
        admin: 'Admin',
        ketoan: 'Kế toán',
        nhanvien: 'Nhân viên',
    };
    return roleNames[role] || role;
}

/**
 * Build menu based on user role
 */
function buildMenu(role) {
    const menuList = document.getElementById('menuList');
    const config = roleMenuConfig[role] || roleMenuConfig['nhanvien'];
    
    menuList.innerHTML = '';
    
    config.forEach(item => {
        const li = document.createElement('li');
        li.className = 'menu-item';
        
        const link = document.createElement('a');
        link.className = 'menu-link';
        if (item.id === 'home') link.classList.add('active');
        link.innerHTML = `${item.icon} ${item.label}`;
        
        link.addEventListener('click', (e) => {
            e.preventDefault();
            showSection(item.id);
            
            // Update active state
            document.querySelectorAll('.menu-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
        
        li.appendChild(link);
        menuList.appendChild(li);
    });
}

/**
 * Show content section
 */
function showSection(sectionId) {
    currentSection = sectionId;
    
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Hide welcome section if not home
    document.getElementById('welcomeSection').style.display = sectionId === 'home' ? 'block' : 'none';
    document.querySelector('.quick-stats').style.display = sectionId === 'home' ? 'grid' : 'none';
    
    // Show selected section
    if (sectionId !== 'home') {
        const section = document.getElementById(`${sectionId}Section`);
        if (section) {
            section.style.display = 'block';
            
            // Load data for section
            if (sectionId === 'employees') loadEmployees();
            else if (sectionId === 'payroll') loadPayrolls();
            else if (sectionId === 'departments') loadDepartments();
            else if (sectionId === 'reports') loadReports();
        }
    }
}

/**
 * Load statistics
 */
async function loadStatistics() {
    try {
        showLoading(true);
        const response = await apiClient.getStatistics();
        
        // Update stat cards
        document.getElementById('stat-employees').querySelector('.stat-number').textContent = 
            response.data.total_employees || 0;
        document.getElementById('stat-departments').querySelector('.stat-number').textContent = 
            response.data.total_departments || 0;
        document.getElementById('stat-payroll').querySelector('.stat-number').textContent = 
            `${formatCurrency(response.data.total_payroll || 0)} đ`;
        
        showLoading(false);
    } catch (error) {
        showLoading(false);
        console.error('Error loading statistics:', error);
        showModal('Lỗi', 'Không thể tải thống kê. Vui lòng kiểm tra Console (F12) để biết chi tiết.');
    }
}

async function loadEmployees() {
    try {
        showLoading(true);
        const response = await apiClient.getEmployees(currentEmployeePage, 20, currentEmployeeSearch);
        
        const tbody = document.getElementById('employeeTableBody');
        tbody.innerHTML = '';
        
        const items = response.data.items || response.data || [];
        
        if (items.length) {
            items.forEach(employee => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${employee.maNV}</td>
                    <td>${employee.tenNV}</td>
                    <td>${employee.email}</td>
                    <td>${employee.tenChucVu || '-'}</td>
                    <td>${employee.tenPhong || '-'}</td>
                    <td>
                        <button class="btn btn-secondary" onclick="editEmployee(${employee.maNV})">Sửa</button>
                        <button class="btn btn-secondary" onclick="deleteEmployee(${employee.maNV})">Xóa</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = `
                <td colspan="6" style="text-align:center; padding: 30px; color: var(--color-text-secondary);">
                    Chưa có dữ liệu nhân viên.
                </td>
            `;
            tbody.appendChild(emptyRow);
        }
        
        showLoading(false);
    } catch (error) {
        showLoading(false);
        showModal('Lỗi', 'Không thể tải danh sách nhân viên');
        console.error(error);
    }
}

/**
 * Load payrolls
 */
async function loadPayrolls() {
    try {
        showLoading(true);
        const monthVal = document.getElementById('payrollMonth').value || new Date().toISOString().slice(0, 7);
        const [year, month] = monthVal.split('-').map(Number);
        
        const response = await apiClient.getPayrolls(month, year, currentPayrollSearch);
        
        const tbody = document.getElementById('payrollTableBody');
        tbody.innerHTML = '';
        
        if (response.data && response.data.length) {
            response.data.forEach(payroll => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${payroll.maBangLuong || payroll.maNV}</td>
                    <td>${payroll.tenNV || 'Nhân viên'}</td>
                    <td>Tháng ${payroll.thang}/${payroll.nam}</td>
                    <td>${formatCurrency(payroll.luongCoBan)} đ</td>
                    <td>${formatCurrency(payroll.thuong || 0)} đ</td>
                    <td>${formatCurrency(payroll.luongThucLinh || 0)} đ</td>
                    <td>
                        <button class="btn btn-secondary" onclick="viewPayroll(${payroll.maBangLuong})">Xem</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = `
                <td colspan="7" style="text-align:center; padding: 30px; color: var(--color-text-secondary);">
                    Chưa có dữ liệu lương của tháng này.
                </td>
            `;
            tbody.appendChild(emptyRow);
        }
        
        showLoading(false);
    } catch (error) {
        showLoading(false);
        console.error('Error loading payrolls:', error);
        showModal('Lỗi', 'Không thể tải dữ liệu lương. Vui lòng kiểm tra Console (F12) để biết chi tiết.');
    }
}

/**
 * Load departments
 */
async function loadDepartments() {
    try {
        showLoading(true);
        const response = await apiClient.getDepartments();
        
        const tbody = document.getElementById('departmentTableBody');
        tbody.innerHTML = '';
        
        if (response.data && response.data.length) {
            response.data.forEach(department => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${department.maPhong}</td>
                    <td>${department.tenPhong}</td>
                    <td>${department.truongPhong || '-'}</td>
                    <td>
                        <button class="btn btn-secondary" onclick="editDepartment(${department.maPhong})">Sửa</button>
                        <button class="btn btn-secondary" onclick="deleteDepartment(${department.maPhong})">Xóa</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = `
                <td colspan="4" style="text-align:center; padding: 30px; color: var(--color-text-secondary);">
                    Chưa có dữ liệu phòng ban.
                </td>
            `;
            tbody.appendChild(emptyRow);
        }
        
        showLoading(false);
    } catch (error) {
        showLoading(false);
        console.error('Error loading departments:', error);
    }
}

/**
 * Load reports
 */
async function loadReports() {
    try {
        showLoading(true);
        const month = document.getElementById('reportMonth').value || new Date().toISOString().slice(0, 7);
        const response = await apiClient.getReport(month);
        
        const reportContent = document.getElementById('reportContent');
        reportContent.innerHTML = `
            <div class="report-summary">
                <p><strong>Tháng báo cáo:</strong> ${month}</p>
                <p><strong>Tổng nhân viên:</strong> ${response.data?.total_employees || 0}</p>
                <p><strong>Tổng lương:</strong> ${formatCurrency(response.data?.total_payroll || 0)} đ</p>
            </div>
        `;
        
        showLoading(false);
    } catch (error) {
        showLoading(false);
        console.error('Error loading report:', error);
    }
}

/**
 * Logout
 */
function logout() {
    if (confirm('Bạn có chắc chắn muốn đăng xuất?')) {
        apiClient.logout();
        window.location.href = 'index.html';
    }
}

/**
 * Show modal
 */
function showModal(title, message, callback = null) {
    const modal = document.getElementById('messageModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    
    modalTitle.textContent = title;
    
    // Support HTML for details - trimming whitespace to ensure it detects the tag
    if (message.trim().startsWith('<')) {
        modalMessage.innerHTML = message;
    } else {
        modalMessage.textContent = message;
    }
    
    modal.classList.add('active');
    window.modalCallback = callback;
}

/**
 * Close modal
 */
function closeModal() {
    const modal = document.getElementById('messageModal');
    modal.classList.remove('active');
    
    if (window.modalCallback) {
        window.modalCallback();
        window.modalCallback = null;
    }
}

/**
 * Show/hide loading
 */
function showLoading(show = true) {
    const spinner = document.getElementById('loadingSpinner');
    if (show) {
        spinner.classList.add('active');
    } else {
        spinner.classList.remove('active');
    }
}

/**
 * Format currency
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('vi-VN').format(value);
}

/**
 * Placeholder functions for future implementation
 */
/**
 * Employee CRUD functions
 */
async function openAddEmployeeForm() {
    try {
        showLoading(true);
        const [deptsRes, posRes] = await Promise.all([
            apiClient.getDepartments(),
            apiClient.getPositions()
        ]);
        
        const depts = deptsRes.data || [];
        const positions = posRes.data || [];
        const today = new Date().toISOString().split('T')[0];
        
        const html = `
            <form id="employeeForm" class="modal-form" onsubmit="event.preventDefault(); saveEmployee();">
                <div class="form-row">
                    <div class="form-group">
                        <label>Tên nhân viên:</label>
                        <input type="text" id="empTenNV" required placeholder="Nguyễn Văn A">
                    </div>
                    <div class="form-group">
                        <label>Ngày sinh:</label>
                        <input type="date" id="empNgaySinh" required value="1995-01-01">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Giới tính:</label>
                        <select id="empGioiTinh">
                            <option value="Nam">Nam</option>
                            <option value="Nữ">Nữ</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Email:</label>
                        <input type="email" id="empEmail" required placeholder="email@example.com">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Số điện thoại:</label>
                        <input type="text" id="empSDT">
                    </div>
                    <div class="form-group">
                        <label>Ngày vào làm:</label>
                        <input type="date" id="empNgayVaoLam" required value="${today}">
                    </div>
                </div>
                <div class="form-group">
                    <label>Địa chỉ:</label>
                    <input type="text" id="empDiaChi">
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Phòng ban:</label>
                        <select id="empMaPhong" required>
                            <option value="">-- Chọn phòng ban --</option>
                            ${depts.map(d => `<option value="${d.maPhong}">${d.tenPhong}</option>`).join('')}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Chức vụ:</label>
                        <select id="empMaChucVu" required>
                            <option value="">-- Chọn chức vụ --</option>
                            ${positions.map(p => `<option value="${p.maChucVu}">${p.tenChucVu}</option>`).join('')}
                        </select>
                    </div>
                </div>
                <div style="margin-top: 10px; display: flex; gap: 10px; justify-content: flex-end;">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">Hủy</button>
                    <button type="submit" class="btn btn-primary">Lưu</button>
                </div>
            </form>
        `;
        
        showLoading(false);
        showModal('Thêm nhân viên mới', html);
    } catch (error) {
        showLoading(false);
        console.error('Error opening add employee form:', error);
        showModal('Lỗi', 'Không thể tải thông tin phòng ban/chức vụ');
    }
}

async function editEmployee(id) {
    try {
        showLoading(true);
        const [empRes, deptsRes, posRes] = await Promise.all([
            apiClient.getEmployee(id),
            apiClient.getDepartments(),
            apiClient.getPositions()
        ]);
        
        const emp = empRes.data;
        const depts = deptsRes.data || [];
        const positions = posRes.data || [];
        
        const html = `
            <form id="employeeForm" class="modal-form" onsubmit="event.preventDefault(); saveEmployee('${id}');">
                <div class="form-row">
                    <div class="form-group">
                        <label>Tên nhân viên:</label>
                        <input type="text" id="empTenNV" value="${emp.TenNV}" required>
                    </div>
                    <div class="form-group">
                        <label>Ngày sinh:</label>
                        <input type="date" id="empNgaySinh" value="${emp.NgaySinh ? emp.NgaySinh.split('T')[0] : ''}" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Giới tính:</label>
                        <select id="empGioiTinh">
                            <option value="Nam" ${emp.GioiTinh === 'Nam' ? 'selected' : ''}>Nam</option>
                            <option value="Nữ" ${emp.GioiTinh === 'Nữ' ? 'selected' : ''}>Nữ</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Email:</label>
                        <input type="email" id="empEmail" value="${emp.Email}" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Số điện thoại:</label>
                        <input type="text" id="empSDT" value="${emp.SDT || ''}">
                    </div>
                    <div class="form-group">
                        <label>Trạng thái:</label>
                        <select id="empTrangThai">
                            <option value="1" ${emp.TrangThai == 1 ? 'selected' : ''}>Đang làm việc</option>
                            <option value="0" ${emp.TrangThai == 0 ? 'selected' : ''}>Đã nghỉ việc</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label>Địa chỉ:</label>
                    <input type="text" id="empDiaChi" value="${emp.DiaChi || ''}">
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Phòng ban:</label>
                        <select id="empMaPhong" required>
                            ${depts.map(d => `<option value="${d.maPhong}" ${d.maPhong == emp.maPhong ? 'selected' : ''}>${d.tenPhong}</option>`).join('')}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Chức vụ:</label>
                        <select id="empMaChucVu" required>
                            ${positions.map(p => `<option value="${p.maChucVu}" ${p.maChucVu == emp.maChucVu ? 'selected' : ''}>${p.tenChucVu}</option>`).join('')}
                        </select>
                    </div>
                </div>
                <div style="margin-top: 10px; display: flex; gap: 10px; justify-content: flex-end;">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">Hủy</button>
                    <button type="submit" class="btn btn-primary">Cập nhật</button>
                </div>
            </form>
        `;
        
        showLoading(false);
        showModal('Sửa thông tin nhân viên', html);
    } catch (error) {
        showLoading(false);
        console.error('Error opening edit employee form:', error);
        showModal('Lỗi', 'Không thể tải thông tin nhân viên');
    }
}

async function saveEmployee(id = null) {
    const data = {
        tenNV: document.getElementById('empTenNV').value,
        ngaySinh: document.getElementById('empNgaySinh').value,
        gioiTinh: document.getElementById('empGioiTinh').value,
        email: document.getElementById('empEmail').value,
        sdt: document.getElementById('empSDT').value,
        diaChi: document.getElementById('empDiaChi').value,
        maPhong: parseInt(document.getElementById('empMaPhong').value),
        maChucVu: parseInt(document.getElementById('empMaChucVu').value),
        trangThai: parseInt(document.getElementById('empTrangThai')?.value || 1)
    };
    
    if (!id) {
        data.ngayVaoLam = document.getElementById('empNgayVaoLam').value;
    }
    
    try {
        showLoading(true);
        let response;
        if (id) {
            response = await apiClient.updateEmployee(id, data);
        } else {
            response = await apiClient.createEmployee(data);
        }
        
        showLoading(false);
        closeModal();
        showModal('Thành công', id ? 'Cập nhật nhân viên thành công!' : 'Thêm nhân viên thành công!', () => {
            loadEmployees();
            loadStatistics();
        });
    } catch (error) {
        showLoading(false);
        console.error('Error saving employee:', error);
        showModal('Lỗi', error.message || 'Không thể lưu thông tin nhân viên');
    }
}

async function deleteEmployee(id) {
    if (confirm('Bạn có chắc chắn muốn xóa nhân viên này? (Dữ liệu liên quan như lương cũng sẽ bị ảnh hưởng)')) {
        try {
            showLoading(true);
            await apiClient.deleteEmployee(id);
            showLoading(false);
            showModal('Thành công', 'Xóa nhân viên thành công!', () => {
                loadEmployees();
                loadStatistics();
            });
        } catch (error) {
            showLoading(false);
            showModal('Lỗi', error.message || 'Không thể xóa nhân viên');
        }
    }
}

function openCalculatePayrollForm() {
    const now = new Date();
    const currentMonth = now.toISOString().slice(0, 7);
    
    const html = `
        <div class="calculate-form">
            <p>Chọn tháng và năm để tính lương cho toàn bộ nhân viên đang hoạt động.</p>
            <div class="form-group" style="margin-top: 15px;">
                <label>Tháng/Năm:</label>
                <input type="month" id="calcMonth" class="search-box" value="${currentMonth}">
            </div>
            <div style="margin-top: 20px; display: flex; gap: 10px; justify-content: flex-end;">
                <button class="btn btn-primary" onclick="startCalculation()">Bắt đầu tính</button>
            </div>
        </div>
    `;
    showModal('Tính lương', html);
}

async function startCalculation() {
    const monthVal = document.getElementById('calcMonth').value;
    if (!monthVal) {
        alert('Vui lòng chọn tháng!');
        return;
    }
    
    const [year, month] = monthVal.split('-').map(Number);
    
    try {
        showLoading(true);
        closeModal(); // Close the input modal
        
        await apiClient.calculatePayroll({
            thang: month,
            nam: year
        });
        
        showLoading(false);
        showModal('Thành công', `Đã tính lương xong cho tháng ${month}/${year}!`, () => {
            if (currentSection === 'payroll') loadPayrolls();
            loadStatistics();
        });
    } catch (error) {
        showLoading(false);
        console.error('Error calculating payroll:', error);
        showModal('Lỗi', error.message || 'Không thể tính lương. Có thể lương tháng này đã được tính trước đó.');
    }
}

async function viewPayroll(id) {
    try {
        showLoading(true);
        const response = await apiClient.getPayrollDetail(id);
        const data = response.data;
        
        const html = `
            <div class="payroll-details">
                <p><strong>Nhân viên:</strong> ${data.tenNV}</p>
                <p><strong>Thời gian:</strong> Tháng ${data.thang}/${data.nam}</p>
                <hr>
                <table class="detail-table">
                    <tr><td>Lương cơ bản:</td><td align="right">${formatCurrency(data.luongCoBan)} đ</td></tr>
                    <tr><td>Phụ cấp chức vụ:</td><td align="right">${formatCurrency(data.phuCapChucVu)} đ</td></tr>
                    <tr><td>Phụ cấp phòng ban:</td><td align="right">${formatCurrency(data.phuCapPhongBan)} đ</td></tr>
                    <tr><td>Tăng ca:</td><td align="right">${formatCurrency(data.tangCa)} đ</td></tr>
                    <tr><td>Thưởng:</td><td align="right">${formatCurrency(data.thuong)} đ</td></tr>
                    <tr class="deduction"><td>Bảo hiểm (10%):</td><td align="right">-${formatCurrency(data.baoHiem)} đ</td></tr>
                    <tr class="deduction"><td>Phạt:</td><td align="right">-${formatCurrency(data.phat)} đ</td></tr>
                    <tr class="total"><td><strong>Thực lĩnh:</strong></td><td align="right"><strong>${formatCurrency(data.luongThucLinh)} đ</strong></td></tr>
                </table>
                ${data.ghiChu ? `<p class="note"><strong>Ghi chú:</strong> ${data.ghiChu}</p>` : ''}
            </div>
        `;
        
        showLoading(false);
        showModal('Chi tiết lương', html);
    } catch (error) {
        showLoading(false);
        console.error('Error viewing payroll:', error);
        showModal('Lỗi', 'Không thể tải chi tiết lương');
    }
}

/**
 * Department CRUD functions
 */
function openAddDepartmentForm() {
    const html = `
        <form id="deptForm" class="modal-form" onsubmit="event.preventDefault(); saveDepartment();">
            <div class="form-group">
                <label>Tên phòng ban:</label>
                <input type="text" id="deptTenPhong" required placeholder="Phòng Kỹ thuật">
            </div>
            <div class="form-group">
                <label>Mô tả:</label>
                <input type="text" id="deptMoTa" placeholder="Khối kỹ thuật và vận hành">
            </div>
            <div style="margin-top: 10px; display: flex; gap: 10px; justify-content: flex-end;">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Hủy</button>
                <button type="submit" class="btn btn-primary">Lưu</button>
            </div>
        </form>
    `;
    showModal('Thêm phòng ban mới', html);
}

async function editDepartment(id) {
    try {
        showLoading(true);
        const response = await apiClient.getDepartment(id);
        const dept = response.data;
        
        const html = `
            <form id="deptForm" class="modal-form" onsubmit="event.preventDefault(); saveDepartment('${id}');">
                <div class="form-group">
                    <label>Tên phòng ban:</label>
                    <input type="text" id="deptTenPhong" value="${dept.tenPhong}" required>
                </div>
                <div class="form-group">
                    <label>Mô tả:</label>
                    <input type="text" id="deptMoTa" value="${dept.moTa || ''}">
                </div>
                <div style="margin-top: 10px; display: flex; gap: 10px; justify-content: flex-end;">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">Hủy</button>
                    <button type="submit" class="btn btn-primary">Cập nhật</button>
                </div>
            </form>
        `;
        
        showLoading(false);
        showModal('Sửa thông tin phòng ban', html);
    } catch (error) {
        showLoading(false);
        console.error('Error opening edit department form:', error);
        showModal('Lỗi', 'Không thể tải thông tin phòng ban');
    }
}

async function saveDepartment(id = null) {
    const data = {
        tenPhong: document.getElementById('deptTenPhong').value,
        moTa: document.getElementById('deptMoTa').value
    };
    
    try {
        showLoading(true);
        let response;
        if (id) {
            response = await apiClient.updateDepartment(id, data);
        } else {
            response = await apiClient.createDepartment(data);
        }
        
        showLoading(false);
        closeModal();
        showModal('Thành công', id ? 'Cập nhật phòng ban thành công!' : 'Thêm phòng ban thành công!', () => {
            loadDepartments();
            loadStatistics();
        });
    } catch (error) {
        showLoading(false);
        console.error('Error saving department:', error);
        showModal('Lỗi', error.message || 'Không thể lưu thông tin phòng ban');
    }
}

async function deleteDepartment(id) {
    if (confirm('Bạn có chắc chắn muốn xóa phòng ban này? (Nhân viên trong phòng ban này sẽ mất liên kết phòng ban)')) {
        try {
            showLoading(true);
            await apiClient.deleteDepartment(id);
            showLoading(false);
            showModal('Thành công', 'Xóa phòng ban thành công!', () => {
                loadDepartments();
                loadStatistics();
            });
        } catch (error) {
            showLoading(false);
            showModal('Lỗi', error.message || 'Không thể xóa phòng ban');
        }
    }
}

function generateReport() {
    showModal('Báo cáo', 'Tạo báo cáo thành công!');
}

function exportReport() {
    showModal('Xuất Excel', 'Chức năng xuất Excel sẽ được phát triển');
}

/**
 * Seed demo data functions
 */
async function seedEmployeesData() {
    if (!confirm('Bạn sẽ tạo dữ liệu mẫu nhân viên. Tiếp tục?')) {
        return;
    }
    
    try {
        showLoading(true);
        const response = await apiClient.seedEmployees();
        showLoading(false);
        
        showModal('Thành công', response.message || 'Tạo dữ liệu nhân viên thành công!', () => {
            loadEmployees();
        });
    } catch (error) {
        showLoading(false);
        showModal('Lỗi', error.message || 'Không thể tạo dữ liệu nhân viên');
        console.error(error);
    }
}

async function seedPayrollsData() {
    if (!confirm('Bạn sẽ tạo dữ liệu mẫu lương. Tiếp tục?')) {
        return;
    }
    
    try {
        showLoading(true);
        const response = await apiClient.seedPayrolls();
        showLoading(false);
        
        showModal('Thành công', response.message || 'Tạo dữ liệu lương thành công!', () => {
            loadPayrolls();
        });
    } catch (error) {
        showLoading(false);
        showModal('Lỗi', error.message || 'Không thể tạo dữ liệu lương');
        console.error(error);
    }
}

async function seedDepartmentsData() {
    if (!confirm('Bạn sẽ tạo dữ liệu mẫu phòng ban. Tiếp tục?')) {
        return;
    }
    
    try {
        showLoading(true);
        const response = await apiClient.seedDepartments();
        showLoading(false);
        
        showModal('Thành công', response.message || 'Tạo dữ liệu phòng ban thành công!', () => {
            loadDepartments();
        });
    } catch (error) {
        showLoading(false);
        showModal('Lỗi', error.message || 'Không thể tạo dữ liệu phòng ban');
        console.error(error);
    }
}

async function seedAllData() {
    if (!confirm('Bạn sẽ tạo TẤT CẢ dữ liệu mẫu (phòng ban, nhân viên, lương). Tiếp tục?')) {
        return;
    }
    
    try {
        showLoading(true);
        const response = await apiClient.seedAll();
        showLoading(false);
        
        const message = `Tạo dữ liệu thành công!
- Phòng ban: ${response.data?.departments || 0}
- Nhân viên: ${response.data?.employees || 0}
- Lương: ${response.data?.payrolls || 0}`;
        
        showModal('Thành công', message, () => {
            loadEmployees();
            loadDepartments();
            loadPayrolls();
            loadStatistics();
        });
    } catch (error) {
        showLoading(false);
        showModal('Lỗi', error.message || 'Không thể tạo dữ liệu');
        console.error(error);
    }
}

/**
 * Close modal on Escape
 */
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});
