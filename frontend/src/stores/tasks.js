import { defineStore } from 'pinia';
import apiClient from '../utils/apiClient';
import { reactive } from 'vue';

export const useTaskStore = defineStore('tasks', {
	state: () => reactive({
		tasks: [], // Список задач (массив объектов)
		filterStatus: '', // Текущий статус фильтра (пустая строка — все задачи, 'true'/'false' — по статусу)
		editingTask: null, // Текущая задача для редактирования (объект или null)
		editedTask: {}, // Данные для редактируемой задачи (копия текущей задачи)
	}),
	actions: {
		async fetchTasks() {
			try {
				const response = await apiClient.get('/get_tasks/'); // Отправляем GET-запрос для получения задач
				this.tasks = response.data; // Сохраняем полученные данные в состояние tasks
			} catch (error) {
				alert(error.response?.data?.detail || 'Произошла ошибка при загрузке задач');
			}
		},
		async addTask(newTask) {
			try {
				console.log('Отправляем новую задачу:', newTask); // Логирование отправляемых данных
				const response = await apiClient.post('/create_task/', newTask); // Отправляем POST-запрос для создания задачи
				this.tasks.push(response.data); // Добавляем новую задачу в локальное состояние
			} catch (error) {
				alert(error.response?.data?.detail || 'Произошла ошибка при добавлении задачи');
			}
		},
		async deleteTask(id) {
			try {
				await apiClient.delete(`/delete_task/${id}/`); // Отправляем DELETE-запрос для удаления задачи
				this.tasks = this.tasks.filter((task) => task.id !== id); // Удаляем задачу из локального состояния
			} catch (error) {
				alert(error.response?.data?.detail || 'Произошла ошибка при удалении задачи');
			}
		},
		editTask(task) {
			this.editingTask = task; // Устанавливаем текущую задачу для редактирования
			this.editedTask = { ...task }; // Создаем копию задачи для временного хранения изменений
		},
		async saveEditedTask() {
			try {
				const response = await apiClient.put(
					`/update_task/${this.editingTask.id}/`,
					this.editedTask
				); // Отправляем PUT-запрос для обновления задачи

				const index = this.tasks.findIndex((task) => task.id === this.editingTask.id); // Находим индекс задачи в массиве

				if (index !== -1) {
					this.tasks[index] = response.data; // Обновляем задачу в локальном состоянии
				}

				this.cancelEdit(); // Заканчиваем редактирование
			} catch (error) {
				alert(error.response?.data?.detail || 'Произошла ошибка при сохранении задачи');
			}
		},
		cancelEdit() {
			this.editingTask = null; // Сбрасываем текущую задачу для редактирования
			this.editedTask = {}; // Очищаем временные данные задачи
		},
		async filterTasks(status) {
			try {
				const response = await apiClient.get(`/filter_by_status/?status=${status}`); // Отправляем GET-запрос для фильтрации
				this.tasks = response.data; // Обновляем список задач в соответствии с фильтром
			} catch (error) {
				alert(error.response?.data?.detail || 'Произошла ошибка при фильтрации задач');
			}
		},
	},
});