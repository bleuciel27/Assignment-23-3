// assets/js/auth.js

const auth = {
    // Configuration
    API_URL: 'http://localhost:8000/api',
    TOKEN_KEY: 'token',
    REFRESH_TOKEN_KEY: 'refresh_token',

    // Login function
    async login(username, password) {
        try {
            const response = await fetch(`${this.API_URL}/token/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }

            const data = await response.json();
            this.setTokens(data.access, data.refresh);
            return true;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },

    // Token management
    setTokens(accessToken, refreshToken) {
        localStorage.setItem(this.TOKEN_KEY, accessToken);
        if (refreshToken) {
            localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
        }
    },

    getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    },

    getRefreshToken() {
        return localStorage.getItem(this.REFRESH_TOKEN_KEY);
    },

    clearTokens() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    },

    // Authentication state
    isAuthenticated() {
        const token = this.getToken();
        return !!token && !this.isTokenExpired(token);
    },

    isTokenExpired(token) {
        if (!token) return true;
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            return payload.exp * 1000 < Date.now();
        } catch (e) {
            return true;
        }
    },

    // Token refresh
    async refreshToken() {
        const refreshToken = this.getRefreshToken();
        if (!refreshToken) return false;

        try {
            const response = await fetch(`${this.API_URL}/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (!response.ok) {
                this.clearTokens();
                return false;
            }

            const data = await response.json();
            this.setTokens(data.access, data.refresh);
            return true;
        } catch (error) {
            console.error('Token refresh error:', error);
            this.clearTokens();
            return false;
        }
    },

    // Authentication headers
    getAuthHeaders() {
        const token = this.getToken();
        return token ? {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        } : {
            'Content-Type': 'application/json'
        };
    },

    // Session management
    async logout() {
        this.clearTokens();
        window.location.href = '/pages/login.html';
    },

    // Request interceptor
    async makeAuthenticatedRequest(url, options = {}) {
        if (this.isTokenExpired(this.getToken())) {
            const refreshed = await this.refreshToken();
            if (!refreshed) {
                this.logout();
                throw new Error('Authentication required');
            }
        }

        const response = await fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                ...this.getAuthHeaders()
            }
        });

        if (response.status === 401) {
            // Token might be expired, try to refresh
            const refreshed = await this.refreshToken();
            if (refreshed) {
                // Retry the request with new token
                return this.makeAuthenticatedRequest(url, options);
            } else {
                this.logout();
                throw new Error('Authentication required');
            }
        }

        return response;
    },

    // Navigation guards
    async checkAuthAndRedirect() {
        if (!this.isAuthenticated()) {
            const refreshed = await this.refreshToken();
            if (!refreshed) {
                window.location.href = '/pages/login.html';
                return false;
            }
        }
        return true;
    },

    // Initialize auth state
    init() {
        if (this.isAuthenticated()) {
            // Update UI or perform any initialization
            return true;
        }
        return this.refreshToken();
    }
};

// Initialize auth when the file loads
auth.init();

// Export the auth object for use in other files
export default auth;