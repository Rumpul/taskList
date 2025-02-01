<template>
	<div class="auth-container">
		<div class="container">
			<h2>Вход</h2>
			<form @submit.prevent="login" class="auth-form">
				<input v-model="loginForm.username" placeholder="Имя пользователя" required />
				<input v-model="loginForm.password" type="password" placeholder="Пароль" required />
				<button type="submit">Войти</button>
			</form>
			<p>
				Нет аккаунта?
				<button @click="switchToRegister" class="link-button">Зарегистрироваться</button>
			</p>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../utils/apiClient';

const loginForm = ref({ username: '', password: '' });
const router = useRouter();

const login = async() => {
	// Проверяем заполненность полей
	if (!loginForm.value.username || !loginForm.value.password) {
		alert('Заполните все поля!');
		return;
	}
	try {
		// Отправляем POST-запрос для логина пользователя и получения токенов
		const response = await apiClient.post('/token/', loginForm.value);
		// Помещаем токены в localStorage
		localStorage.setItem('access_token', response.data.access);
		localStorage.setItem('refresh_token', response.data.refresh);
		// Перенаправляем на страницу с задачами
		router.push('/tasks');
	} catch (error) {
		alert(error.response?.data?.detail || 'Неверные данные для входа');
	}
}
function switchToRegister() {
	router.push('/registration');
}
</script>

<style scoped>
.auth-container {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
}

.container {
	padding: 25px;
	border-radius: 12px;
	box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
	background: white;
	width: 100%;
	max-width: 400px;
}

h2 {
	margin-bottom: 20px;
}

.auth-form {
	display: flex;
	flex-direction: column;
	align-items: center;
}

button {
	width: 100%;
	max-width: 300px;
}
</style>