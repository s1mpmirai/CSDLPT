/**
 * Login Page JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        const role = document.getElementById('role').value;
        
        if (!username || !password) {
            showModal('Lỗi', 'Vui lòng nhập tên đăng nhập và mật khẩu');
            return;
        }
        
        await login(username, password, role);
    });
});

/**
 * Login function
 */
async function login(username, password, role) {
    try {
        showLoading(true);
        
        const response = await apiClient.login(username, password, role);
        
        if (response.success) {
            const user = {
                username: username,
                role: response.role || role,
                name: response.name || 'User',
                maNV: response.maNV
            };
            localStorage.setItem(CONFIG.ADVANCED.USER_KEY, JSON.stringify(user));
            localStorage.setItem(CONFIG.ADVANCED.TOKEN_KEY, response.token);
        }

        showLoading(false);
        showModal('Thành công', 'Đăng nhập thành công!', () => {
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        });
    } catch (error) {
        showLoading(false);
        showModal('Lỗi đăng nhập', error.message || 'Tên đăng nhập hoặc mật khẩu không đúng');
        console.error(error);
    }
}

/**
 * Show message modal
 */
function showModal(title, message, callback = null) {
    const modal = document.getElementById('messageModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    
    modal.classList.add('active');
    
    // Store callback for OK button
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
 * Show/hide loading spinner
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
 * Close modal on Escape key
 */
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});
