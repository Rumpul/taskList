<template>
	<div class="task-list-container">
		<div class="container">
			<div class="header-wrapper">
				<h2>Список задач</h2>
				<button @click="logout" class="logout-button">Выйти</button>
			</div>

			<form @submit.prevent="handleAddTask" class="task-form">
				<input v-model="newTask.title" placeholder="Название задачи" required />
				<textarea v-model="newTask.description" placeholder="Описание задачи"></textarea>
				<button type="submit">Добавить задачу</button>
			</form>

			<div class="filter-container">
				<label for="filter">Фильтр:</label>
				<select v-model="filterStatus" @change="filterTasks" id="filter">
					<option value="">Все</option>
					<option value="true">Выполнено</option>
					<option value="false">Не выполнено</option>
				</select>
			</div>

			<div class="task-table-container">
				<table class="task-table">
					<thead>
						<tr>
							<th>Название</th>
							<th>Статус</th>
							<th>Дата создания</th>
							<th>Дата выполнения</th>
							<th>Действия</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="task in tasks" :key="task.id" class="task-row">
							<td>{{ task.title }}</td>
							<td>{{ task.status ? 'Выполнено' : 'Не выполнено' }}</td>
							<td>{{ formatDate(task.created_at) }}</td>
							<td>{{ formatDate(task.due_date) }}</td>
							<td>
								<div class="table-btn">
									<button @click="editTask(task)" class="edit-button">Редактировать</button>
									<button @click="deleteTask(task.id)" class="delete-button">Удалить</button>
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<div v-if="editingTask" class="modal">
				<div class="modal-content">
					<h3>Редактирование задачи</h3>
					<form @submit.prevent="saveEditedTask">
						<input v-model="editedTask.title" placeholder="Название задачи" required />
						<textarea v-model="editedTask.description" placeholder="Описание задачи"></textarea>
						<label>
							Статус:
							<select v-model="editedTask.status">
								<option :value="true">Выполнено</option>
								<option :value="false">Не выполнено</option>
							</select>
						</label>
						<label>
							Дата выполнения:
							<input type="date" v-model="editedTask.due_date" />
						</label>
						<button type="submit" class="save-button">Сохранить</button>
						<button @click="cancelEdit" class="cancel-button">Отмена</button>
					</form>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { storeToRefs } from 'pinia';

import { useTaskStore } from '../stores/tasks';
import apiClient from '../utils/apiClient';

// Инициализируем хранилище и роутер
const taskStore = useTaskStore();
const router = useRouter();

const newTask = ref({ title: '', description: '' });

// Применяем реактивность для параметров хранилища
const { tasks, filterStatus, editingTask, editedTask } = storeToRefs(taskStore);

async function logout() {
	// Функция залогирования пользователя
	try {
		const refreshToken = localStorage.getItem('refresh_token');
		if (!refreshToken) {
			alert('Вы уже вышли из системы.');
			router.push('/');
			return;
		}
		await apiClient.post('/logout/', { refresh_token: refreshToken });

		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');

		alert('Вы успешно вышли из системы.');
		router.push('/');
	} catch (error) {
		console.error('Ошибка при выходе:', error);
		alert('Произошла ошибка при выходе из системы. Пожалуйста, попробуйте снова.');
		router.push('/');
	}
}

const handleAddTask = async () => {
	if (!newTask.value.title || !newTask.value.description) {
		// Проверяем заполненность полей
		alert('Заполните все поля!');
		return;
	}

	try {
		// Отправляем задание
		await taskStore.addTask({ ...newTask.value });
		// Очищаем поля задания
		newTask.value = { title: '', description: '' };
	} catch (error) {
		// Обрабатываем и логируем ошибку в консоль
		console.error('Ошибка при создании задачи:', error);
		// Обрабатываем и отправляем ошибку пользователю
		alert(error.response?.data?.detail || 'Произошла ошибка при создании задачи.');
	}
};
const filterTasks = async () => {
	try {
		// Запрос на фильтрацию
		await taskStore.filterTasks(filterStatus.value);
	} catch (error) {
		console.error('Ошибка при фильтрации задач:', error);
		alert(error.response?.data?.detail || 'Ошибка при фильтрации задач.');
	}
};

const formatDate = (date) => {
	if (!date) return '';
	const options = { year: 'numeric', month: 'numeric', day: 'numeric' };
	return new Date(date).toLocaleDateString('ru-RU', options);
};

const deleteTask = (id) => taskStore.deleteTask(id);
const editTask = (task) => taskStore.editTask(task);
const saveEditedTask = () => taskStore.saveEditedTask();
const cancelEdit = () => taskStore.cancelEdit();


taskStore.fetchTasks();
</script>

<style scoped>

.task-table-container {
	overflow-y: auto;
	max-height: 400px;
	margin-top: 20px;
	border: 1px solid #ccc;
	border-radius: 8px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.task-table {
	width: 100%;
	border-collapse: collapse;
	text-align: left;
}

.task-table th,
.task-table td {
	text-align: center;
	padding: 10px;
	border-bottom: 1px solid #ddd;
}

.task-table th {
	background-color: #f4f4f9;
	font-weight: bold;
}

.task-table .task-row:hover {
	background-color: #f9f9f9;
	cursor: pointer;
}

.task-actions button {
	margin-right: 10px;
}

.edit-button {
	background-color: #28a745;
	color: white;
}

.delete-button {
	background-color: #dc3545;
	color: white;
}

.modal {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	justify-content: center;
	align-items: center;
}

.modal-content {
	background: white;
	padding: 25px;
	border-radius: 12px;
	box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
	width: 400px;
	max-width: 90%;
	animation: fadeIn 0.3s ease-in-out;
}
.table-btn{
	display: flex;
}
@keyframes fadeIn {
	from {
		opacity: 0;
		transform: scale(0.9);
	}

	to {
		opacity: 1;
		transform: scale(1);
	}
}

@media (max-width: 600px) {
	.container {
		padding: 15px;
	}

	.task-table th,
	.task-table td {
		font-size: 14px;
		padding: 8px;
	}
}
</style>