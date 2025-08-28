class OneClickAPI {
    constructor() {
        this.baseURL = 'http://localhost:5000/api';
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                ...options.headers,
            },
            credentials: 'include', // This is crucial for cookies
            ...options,
        };

        if (options.body) {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);
            
            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            let data;
            
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }
            
            if (!response.ok) {
                throw new Error(data.message || `API request failed: ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    // Auth methods
    async register(email, password, fullName) {
        return this.request('/register', {
            method: 'POST',
            body: { email, password, fullName }
        });
    }

    async login(email, password) {
        return this.request('/login', {
            method: 'POST',
            body: { email, password }
        });
    }

    async logout() {
        const result = await this.request('/logout', {
            method: 'POST'
        });
        
        // Clear client-side session data
        localStorage.removeItem('user');
        sessionStorage.removeItem('user');
        
        return result;
    }

    async getCurrentUser() {
        try {
            return await this.request('/user');
        } catch (error) {
            // If not authenticated, clear local data
            if (error.message.includes('401') || error.message.includes('Not authenticated')) {
                localStorage.removeItem('user');
                sessionStorage.removeItem('user');
            }
            throw error;
        }
    }

    // Profile management methods
    async updateProfile(userData) {
        try {
            const result = await this.request('/user/update', {
                method: 'PUT',
                body: userData // e.g., { full_name: "New Name" }
            });
            
            // Update local storage with new user data if successful
            if (result.success && result.user) {
                this.setLocalUser(result.user);
            }
            
            return result;
        } catch (error) {
            console.error('Profile update error:', error);
            throw error;
        }
    }

    async changePassword(currentPassword, newPassword) {
        try {
            return await this.request('/user/change-password', {
                method: 'POST',
                body: { 
                    current_password: currentPassword, 
                    new_password: newPassword 
                }
            });
        } catch (error) {
            console.error('Password change error:', error);
            throw error;
        }
    }

    // Avatar upload method (placeholder for future Supabase Storage integration)
    async uploadAvatar(file) {
        try {
            // This would typically involve:
            // 1. Upload file to Supabase Storage
            // 2. Get the public URL
            // 3. Update user's avatar_url in the database
            // For now, this is a placeholder
            
            console.warn('Avatar upload not yet implemented - requires Supabase Storage setup');
            
            // Simulate success for development
            return {
                success: false,
                message: 'Avatar upload feature coming soon! Supabase Storage integration needed.'
            };
        } catch (error) {
            console.error('Avatar upload error:', error);
            throw error;
        }
    }

    // User session management
    isAuthenticated() {
        return localStorage.getItem('user') !== null;
    }

    getLocalUser() {
        const userData = localStorage.getItem('user');
        return userData ? JSON.parse(userData) : null;
    }

    setLocalUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    }

    clearLocalUser() {
        localStorage.removeItem('user');
        sessionStorage.removeItem('user');
    }

    // Utility methods for better user experience
    async refreshUserData() {
        try {
            const data = await this.getCurrentUser();
            if (data.success) {
                this.setLocalUser(data.user);
                return data.user;
            }
            throw new Error(data.message || 'Failed to refresh user data');
        } catch (error) {
            console.error('Error refreshing user data:', error);
            throw error;
        }
    }

    // Method to check if session is still valid
    async validateSession() {
        try {
            const data = await this.getCurrentUser();
            return data.success;
        } catch (error) {
            console.error('Session validation failed:', error);
            return false;
        }
    }

    // Helper method for handling authentication redirects
    redirectToLogin(message = 'Please log in to continue') {
        this.clearLocalUser();
        alert(message);
        window.location.href = 'login.html';
    }

    // Helper method for handling successful authentication
    handleAuthSuccess(user, redirectUrl = 'dashboard.html') {
        this.setLocalUser(user);
        window.location.href = redirectUrl;
    }

    // Method to get user's display name
    getUserDisplayName(user = null) {
        const currentUser = user || this.getLocalUser();
        if (!currentUser) return 'User';
        
        return currentUser.full_name || currentUser.email.split('@')[0] || 'User';
    }

    // Method to get user's avatar URL
    getUserAvatarUrl(user = null) {
        const currentUser = user || this.getLocalUser();
        if (!currentUser) return 'https://ui-avatars.com/api/?name=User&background=4361ee&color=fff';
        
        return currentUser.avatar_url || 
               `https://ui-avatars.com/api/?name=${encodeURIComponent(currentUser.full_name || currentUser.email)}&background=4361ee&color=fff`;
    }

    // Method for handling API errors gracefully
    handleApiError(error, context = 'API operation') {
        console.error(`${context} failed:`, error);
        
        // Handle specific error types
        if (error.message.includes('401') || error.message.includes('Not authenticated')) {
            this.redirectToLogin('Your session has expired. Please log in again.');
            return;
        }
        
        if (error.message.includes('403')) {
            alert('You do not have permission to perform this action.');
            return;
        }
        
        if (error.message.includes('500')) {
            alert('Server error occurred. Please try again later.');
            return;
        }
        
        // Generic error handling
        alert(`${context} failed: ${error.message}`);
    }

    // Method to format dates consistently
    formatDate(dateString) {
        if (!dateString) return 'Unknown';
        
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        } catch (error) {
            console.error('Date formatting error:', error);
            return 'Invalid Date';
        }
    }

    // Method to safely update UI elements
    updateElement(elementId, content, attribute = 'textContent') {
        try {
            const element = document.getElementById(elementId);
            if (element) {
                if (attribute === 'src' || attribute === 'href') {
                    element[attribute] = content;
                } else {
                    element[attribute] = content;
                }
            } else {
                console.warn(`Element with ID '${elementId}' not found`);
            }
        } catch (error) {
            console.error(`Error updating element ${elementId}:`, error);
        }
    }

    // Method to safely update multiple elements (useful for avatars across the page)
    updateElements(selector, content, attribute = 'textContent') {
        try {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (attribute === 'src' || attribute === 'href') {
                    element[attribute] = content;
                } else {
                    element[attribute] = content;
                }
            });
        } catch (error) {
            console.error(`Error updating elements with selector '${selector}':`, error);
        }
    }
}

// Create global API instance
window.oneClickAPI = new OneClickAPI();

// Optional: Add some global helper functions for common operations
window.updateUserUI = function(user) {
    const api = window.oneClickAPI;
    
    // Update user name elements
    api.updateElement('userName', api.getUserDisplayName(user));
    api.updateElement('userEmail', user.email);
    api.updateElement('welcomeName', api.getUserDisplayName(user));
    api.updateElement('profileName', api.getUserDisplayName(user));
    api.updateElement('profileEmail', user.email);
    
    // Update avatar elements
    const avatarUrl = api.getUserAvatarUrl(user);
    api.updateElements('#userAvatar, #mobileUserAvatar, .user-avatar-sm img, #profileAvatar', avatarUrl, 'src');
    
    // Update member since date if element exists
    if (user.created_at) {
        api.updateElement('memberSince', api.formatDate(user.created_at));
    }
};

// Optional: Add authentication check for protected pages
window.checkAuth = function(redirectToLogin = true) {
    const api = window.oneClickAPI;
    const user = api.getLocalUser();
    
    if (!user && redirectToLogin) {
        api.redirectToLogin('Please log in to access this page.');
        return false;
    }
    
    return !!user;
};

// Optional: Add logout confirmation helper
window.confirmLogout = async function() {
    if (confirm('Are you sure you want to logout?')) {
        try {
            await window.oneClickAPI.logout();
            alert('Logout successful!');
            window.location.href = 'index.html';
        } catch (error) {
            console.error('Logout error:', error);
            alert('Logout failed. Please try again.');
            // Even if API fails, clear local storage and redirect for better UX
            window.oneClickAPI.clearLocalUser();
            window.location.href = 'index.html';
        }
    }
};
