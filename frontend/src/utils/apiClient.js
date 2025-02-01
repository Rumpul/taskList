import axios from 'axios';

const apiClient = axios.create({
	baseURL: 'http://localhost:8000/api/',
	headers: {
		'Content-Type': 'application/json',
	},
});

let isRefreshing = false;
let refreshQueue = [];

apiClient.interceptors.request.use(
	// Перехватываем запрос
	(config) => {
		const accessToken = localStorage.getItem('access_token');
		if (accessToken) {
			config.headers.Authorization = `Bearer ${accessToken}`;
		}
		return config;
	},
	(error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
	response => response,
	async error => {
		const originalRequest = error.config;

		// Проверяем только 401 ошибку
		if (error.response?.status === 401 && !originalRequest._retry) {

			originalRequest._retry = true;

			// Если уже в процессе обновления - ставим в очередь
			if (isRefreshing) {
				return new Promise((resolve) => {
					refreshQueue.push(() => {
						originalRequest.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`;
						resolve(apiClient(originalRequest));
					});
				});
			}

			isRefreshing = true;

			try {
				const { data } = await apiClient.post('token/refresh/', {
					refresh: localStorage.getItem('refresh_token')
				});

				// Обновляем токены
				localStorage.setItem('access_token', data.access);
				if (data.refresh) {
					localStorage.setItem('refresh_token', data.refresh);
				}

				// Обновляем дефолтный заголовок
				apiClient.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;

				// Перезапускаем очередь
				refreshQueue.forEach(callback => callback());
				refreshQueue = [];

				// Повторяем оригинальный запрос
				originalRequest.headers.Authorization = `Bearer ${data.access}`;
				return apiClient(originalRequest);

			} catch (refreshError) {
				// Полный сброс при ошибке обновления
				localStorage.removeItem('access_token');
				localStorage.removeItem('refresh_token');
				window.location.href = '/login';
				return Promise.reject(refreshError);
			} finally {
				isRefreshing = false;
			}
		}

		return Promise.reject(error);
	}
);

export default apiClient;