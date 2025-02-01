<template>
	<div class="auth-container">
		<div class="container">
			<h2>Регистрация</h2>
			<form @submit.prevent="register" class="auth-form">
				<input v-model="registerForm.username" placeholder="Имя пользователя" required />
				<input v-model="registerForm.password" type="password" placeholder="Пароль" required />
				<button type="submit">Зарегистрироваться</button>
			</form>
			<p>
				Уже есть аккаунт?
				<button @click="switchToLogin" class="link-button">Войти</button>
			</p>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../utils/apiClient';

const registerForm = ref({ username: '', password: '' });
const router = useRouter();
const register = async() => {
	// Проверяем заполненность полей
	if (!registerForm.value.username || !registerForm.value.password) {
		alert('Заполните все поля!');
		return;
	}
	try {
		// Отправляем POST-запрос для регистрации пользователя
		const response = await apiClient.post('/users/', registerForm.value);
		alert('Вы успешно зарегистрированы!');
		// Перенаправляем на главную страницу
		router.push('/');
	} catch (error) {
		alert(error.response?.data || 'Произошла ошибка при регистрации');
	}
}
function switchToLogin() {
	router.push('/');
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