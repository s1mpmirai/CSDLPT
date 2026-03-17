/**
 * API Client for HR Payroll System
 * Handles all communication with the Flask backend
 */

class PayrollAPIClient {
    constructor(baseUrl = null) {
        // Use baseUrl from config if not provided
        this.baseUrl = baseUrl || (CONFIG && CONFIG.API.BASE_URL) || 'http://localhost:5000';
        this.token = localStorage.getItem(CONFIG?.ADVANCED?.TOKEN_KEY || 'token') || null;
        this.user = JSON.parse(localStorage.getItem(CONFIG?.ADVANCED?.USER_KEY || 'user') || 'null');
        
        if (CONFIG?.DEBUG?.LOG_REQUESTS) {
            console.log(`✓ PayrollAPIClient initialized with baseUrl: ${this.baseUrl}`);
        }
    }

    /**
     * Make HTTP request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        // Add authorization header if token exists
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            method: options.method || 'GET',
            headers,
            ...options,
        };

        if (options.body) {
            config.body = JSON.stringify(options.body);
        }

        try {
            if (CONFIG?.DEBUG?.LOG_REQUESTS) {
            console.log(`→ API Request: ${config.method} ${url}`, config);
        }

        const response = await fetch(url, config);

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            const errMsg = error.message || `HTTP ${response.status}`;
            if (CONFIG?.DEBUG?.LOG_RESPONSES) {
                console.warn(`← API Response error: ${config.method} ${url}`, response.status, errMsg, error);
            }
            throw new Error(errMsg);
        }

        const json = await response.json();
        if (CONFIG?.DEBUG?.LOG_RESPONSES) {
            console.log(`← API Response: ${config.method} ${url}`, response.status, json);
        }
        return json;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

    /**
     * Authentication APIs
     */
    async login(username, password, role) {
        const response = await this.request('/api/auth/login', {
            method: 'POST',
            body: { username, password, role },
        });

        // If backend returns { success: ..., token: ..., user: ... }
        if (!response || response.success === false) {
            throw new Error(response?.message || 'Login failed');
        }

        // Save token and user data
        // Backend may return token in different shapes - support common patterns
        this.token = response.token ?? response.access_token ?? response.data?.token ?? response.data?.access_token ?? null;
        this.user = response.user ?? response.data?.user ?? null;
        
        if (!this.token) {
            console.error('Login response did not include a token:', response);
            throw new Error('Không nhận được access token từ server');
        }

        const tokenKey = CONFIG?.ADVANCED?.TOKEN_KEY || 'token';
        const userKey = CONFIG?.ADVANCED?.USER_KEY || 'user';
        
        localStorage.setItem(tokenKey, this.token);
        localStorage.setItem(userKey, JSON.stringify(this.user));

        if (CONFIG?.DEBUG?.LOG_RESPONSES) {
            console.log('✓ Login successful:', this.user);
        }

        return response;
    }

    logout() {
        this.token = null;
        this.user = null;
        
        const tokenKey = CONFIG?.ADVANCED?.TOKEN_KEY || 'token';
        const userKey = CONFIG?.ADVANCED?.USER_KEY || 'user';
        
        localStorage.removeItem(tokenKey);
        localStorage.removeItem(userKey);
        
        if (CONFIG?.DEBUG?.LOG_RESPONSES) {
            console.log('✓ Logout successful');
        }
    }

    /**
     * Employee APIs
     */
    async getEmployees(page = 1, pageSize = 20, q = '') {
        let url = `/api/nhanvien?page=${page}&limit=${pageSize}&trangThai=1`;
        if (q) url += `&q=${encodeURIComponent(q)}`;
        return this.request(url);
    }

    async getEmployee(id) {
        return this.request(`/api/nhanvien/${id}`);
    }

    async createEmployee(data) {
        return this.request('/api/nhanvien', {
            method: 'POST',
            body: data,
        });
    }

    async updateEmployee(id, data) {
        return this.request(`/api/nhanvien/${id}`, {
            method: 'PUT',
            body: data,
        });
    }

    async deleteEmployee(id) {
        return this.request(`/api/nhanvien/${id}`, {
            method: 'DELETE',
        });
    }

    /**
     * Payroll APIs
     */
    async getPayrolls(month, year, q = '') {
        let url = `/api/luong/danh-sach?thang=${month}&nam=${year}`;
        if (q) url += `&q=${encodeURIComponent(q)}`;
        return this.request(url);
    }

    async getPayroll(id) {
        return this.request(`/api/luong/chi-tiet/id/${id}`);
    }

    async getPayrollDetail(id) {
        return this.request(`/api/luong/chi-tiet/id/${id}`);
    }

    async calculatePayroll(data) {
        return this.request('/api/luong/chi-tiet', {
            method: 'POST',
            body: data,
        });
    }

    async updatePayroll(id, data) {
        return this.request(`/api/luong/${id}`, {
            method: 'PUT',
            body: data,
        });
    }

    /**
     * Department APIs
     */
    async getDepartments() {
        return this.request('/api/phongban');
    }

    async getDepartment(id) {
        return this.request(`/api/phongban/${id}`);
    }

    async createDepartment(data) {
        return this.request('/api/phongban', {
            method: 'POST',
            body: data,
        });
    }

    async updateDepartment(id, data) {
        return this.request(`/api/phongban/${id}`, {
            method: 'PUT',
            body: data,
        });
    }

    async deleteDepartment(id) {
        return this.request(`/api/phongban/${id}`, {
            method: 'DELETE',
        });
    }

    /**
     * Position APIs
     */
    async getPositions() {
        return this.request('/api/chucvu');
    }

    /**
     * Statistics APIs
     */
    async getStatistics() {
        return this.request('/api/statistics');
    }

    /**
     * Report APIs
     */
    async getReport(month) {
        return this.request(`/api/reports/payroll?month=${month}`);
    }

    /**
     * Seed/Demo Data APIs
     */
    async seedAll() {
        return this.request('/api/seed/all', {
            method: 'POST',
        });
    }

    async seedEmployees() {
        return this.request('/api/seed/employees', {
            method: 'POST',
        });
    }

    async seedDepartments() {
        return this.request('/api/seed/departments', {
            method: 'POST',
        });
    }

    async seedPayrolls() {
        return this.request('/api/seed/payrolls', {
            method: 'POST',
        });
    }
}

// Create global instance
const apiClient = new PayrollAPIClient();
