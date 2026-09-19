const API = {
    getToken() {
        return localStorage.getItem('medicare_token');
    },

    getUser() {
        const u = localStorage.getItem('medicare_user');
        return u ? JSON.parse(u) : null;
    },

    setAuth(token, user) {
        localStorage.setItem('medicare_token', token);
        localStorage.setItem('medicare_user', JSON.stringify(user));
    },

    clearAuth() {
        localStorage.removeItem('medicare_token');
        localStorage.removeItem('medicare_user');
    },

    logout() {
        this.clearAuth();
        window.location.href = '/login';
    },

    async request(url, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        };

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const res = await fetch(url, { ...options, headers });
            const data = await res.json();

            if (res.status === 401) {
                // Token invalid or expired
                if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register') && window.location.pathname !== '/') {
                    this.clearAuth();
                    window.location.href = '/login?expired=1';
                }
            }

            if (!res.ok) {
                const errorMsg = (data && data.error && data.error.message) || data.message || 'An error occurred';
                throw new Error(errorMsg);
            }

            return data;
        } catch (err) {
            console.error('API Request Error:', err);
            throw err;
        }
    },

    get(url) {
        return this.request(url, { method: 'GET' });
    },

    post(url, body) {
        return this.request(url, { method: 'POST', body: JSON.stringify(body) });
    },

    put(url, body) {
        return this.request(url, { method: 'PUT', body: JSON.stringify(body) });
    },

    delete(url) {
        return this.request(url, { method: 'DELETE' });
    },

    requireAuth(allowedRoles = null) {
        const user = this.getUser();
        const token = this.getToken();

        if (!token || !user) {
            window.location.href = '/login';
            return false;
        }

        if (allowedRoles) {
            const roles = Array.isArray(allowedRoles) ? allowedRoles : [allowedRoles];
            if (!roles.includes(user.role)) {
                alert(`Access restricted. You need ${roles.join(' or ')} privileges.`);
                this.redirectByRole(user.role);
                return false;
            }
        }
        return true;
    },

    redirectByRole(role) {
        if (role === 'patient') {
            window.location.href = '/patient/dashboard';
        } else if (role === 'doctor') {
            window.location.href = '/doctor/dashboard';
        } else if (role === 'admin') {
            window.location.href = '/admin/dashboard';
        } else {
            window.location.href = '/';
        }
    },

    showAlert(elementId, message, type = 'danger') {
        const el = document.getElementById(elementId);
        if (!el) return;
        el.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }
};

// Global UI setup
document.addEventListener('DOMContentLoaded', () => {
    const user = API.getUser();
    const userNav = document.getElementById('nav-user-info');
    if (userNav && user) {
        userNav.innerHTML = `
            <span class="badge bg-primary me-2">${user.role.toUpperCase()}</span>
            <span class="text-dark fw-bold me-3">${user.name}</span>
            <button class="btn btn-outline-danger btn-sm" onclick="API.logout()">Logout</button>
        `;
    }
});
