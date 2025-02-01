import { createRouter, createWebHistory } from 'vue-router';
import Auth from '../components/Auth.vue';
import Register from '../components/Register.vue';
import TaskList from '../components/TaskList.vue';

const routes = [
	{ path: '/', component: Auth },
	{ path: '/registration', component: Register, name: 'register' },
	{ path: '/tasks', component: TaskList },
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
