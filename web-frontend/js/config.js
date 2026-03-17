/**
 * Configuration File for HR Payroll Web Frontend
 * Edit this file to change settings for your environment
 */

const CONFIG = {
    // ===== API SETTINGS =====
    API: {
        // Base URL của Flask backend
        BASE_URL: 'http://localhost:5000',
        
        // Timeout cho API requests (milliseconds)
        TIMEOUT: 30000,
        
        // Retry failed requests
        RETRY_ENABLED: false,
        RETRY_ATTEMPTS: 3,
    },

    // ===== UI SETTINGS =====
    UI: {
        // Số item per page trong tables
        PAGE_SIZE: 20,
        
        // Theme colors (có thể thay bằng CSS variables)
        PRIMARY_COLOR: '#4a99ff',
        SECONDARY_COLOR: '#333333',
        ERROR_COLOR: '#ff4444',
        SUCCESS_COLOR: '#44aa44',
    },

    // ===== FEATURES =====
    FEATURES: {
        // Bật/tắt features theo role
        ADMIN: {
            EMPLOYEES: true,
            PAYROLL: true,
            DEPARTMENTS: true,
            REPORTS: true,
            USERS: true,
            SETTINGS: false,
        },
        KETOAN: {
            EMPLOYEES: false,
            PAYROLL: true,
            DEPARTMENTS: false,
            REPORTS: true,
            USERS: false,
            SETTINGS: false,
        },
        NHANVIEN: {
            EMPLOYEES: false,
            PAYROLL: true,
            DEPARTMENTS: false,
            REPORTS: false,
            USERS: false,
            SETTINGS: false,
        },
    },

    // ===== LOCALE SETTINGS =====
    LOCALE: {
        LANGUAGE: 'vi',  // 'vi' hoặc 'en'
        DATE_FORMAT: 'DD/MM/YYYY',
        CURRENCY: 'VND',
    },

    // ===== DEBUG SETTINGS =====
    DEBUG: {
        // Log API requests
        LOG_REQUESTS: true,
        
        // Log API responses
        LOG_RESPONSES: false,
        
        // Show debug messages in console
        VERBOSE: false,
    },

    // ===== ADVANCED =====
    ADVANCED: {
        // Local storage key untuk token
        TOKEN_KEY: 'token',
        
        // Local storage key untuk user data
        USER_KEY: 'user',
        
        // Redirect to login after inactivity (0 = disabled)
        INACTIVITY_TIMEOUT: 0,  // milliseconds
        
        // Enable debug mode
        DEBUG_MODE: false,
    },
};

/**
 * Function để lấy config value
 */
function getConfig(path) {
    return CONFIG[path] || null;
}

/**
 * Function để update API base URL
 */
function setApiBaseUrl(url) {
    CONFIG.API.BASE_URL = url;
    console.log(`✓ API Base URL changed to: ${url}`);
}

/**
 * Export cho các file khác
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CONFIG, getConfig, setApiBaseUrl };
}
