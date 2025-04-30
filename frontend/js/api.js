// Базовый URL API
const API_URL = 'http://localhost:8000';

// Функция для работы с API
async function apiRequest(endpoint, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    // Если есть токен в localStorage, добавляем его в заголовки
    const token = localStorage.getItem('token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method,
        headers,
        // Удаляем credentials, так как это может вызывать проблемы с CORS
        // credentials: 'include'
    };

    if (data) {
        config.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Произошла ошибка');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// API методы для работы с пользователями
const userApi = {
    // Регистрация пользователя
    async register(userData) {
        return await apiRequest('/user/register', 'POST', userData);
    },

    // Вход пользователя
    async login(credentials) {
        return await apiRequest('/user/login', 'POST', credentials);
    },

    // Получение информации о текущем пользователе
    async getCurrentUser() {
        return await apiRequest('/user/me', 'GET');
    }
};

// Экспортируем API методы
window.userApi = userApi; 