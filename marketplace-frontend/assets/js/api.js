// assets/js/api.js
const api = {
    async makeAuthenticatedRequest(url, options = {}) {
        const token = localStorage.getItem('token');
        
        if (auth.isTokenExpired(token)) {
            const refreshed = await auth.refreshToken();
            if (!refreshed) {
                throw new Error('Authentication required');
            }
        }

        const response = await fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                ...auth.getAuthHeaders()
            }
        });

        if (response.status === 401) {
            // Token might be expired, try to refresh
            const refreshed = await auth.refreshToken();
            if (refreshed) {
                // Retry the request with new token
                return this.makeAuthenticatedRequest(url, options);
            } else {
                throw new Error('Authentication required');
            }
        }

        return response;
    },

    async login(username, password) {
        return auth.login(username, password);
    }
};