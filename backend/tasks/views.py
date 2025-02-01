from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from .models import Task
from .serializers import UserSerializer, TaskSerializer

# Create your views here.

class UserViewSet(views.APIView):
		def post(self, request, *args, **kwargs):
				# Регистрируем/сохраняем пользователя
				serializer = UserSerializer(data=request.data)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		
class LogoutView(views.APIView):
		# Проверяем прошел ли пользователь аунтификацию
		permission_classes = [IsAuthenticated]
		def post(self, request):
				try:
						refresh_token = request.data.get('refresh_token')
						if refresh_token is None:
								return Response({'error': 'Не предоставлен refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
						token = RefreshToken(refresh_token)
						# Помещаем токен в черный список
						token.blacklist()
						return Response({'detail': 'Вы успешно вышли из системы.'}, status=status.HTTP_200_OK)
				except Exception as e:
						return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)\

class TaskViewSet(viewsets.ViewSet):
		# Проверяем прошел ли пользователь аунтификацию
		permission_classes = [IsAuthenticated]

		def get_tasks(self, request):
			# Получаем список заданий текущего пользователя
			queryset = Task.objects.filter(user=request.user.id)
			serializer_for_queryset = TaskSerializer(
					instance=queryset,
					many=True
			)
			return Response(serializer_for_queryset.data, status=status.HTTP_200_OK)

		def create_task(self, request, *args, **kwargs):
				# Создаем задание
				request.data["user"] = request.user.id # Получаем id текущего пользователя и помещаем его в данные запроса
				serializer = TaskSerializer(data=request.data)
				serializer.is_valid(raise_exception=True) # Валидация данных и поднятие ошибки в случае не корректных данных
				serializer.save() # Сохранение задачи в БД
				return Response(serializer.data, status=status.HTTP_201_CREATED)

		def update_task(self, request, *args, **kwargs):
				# Обновляем задание
				pk = kwargs.get('pk', None) # Получаем id задания
				curr_user = request.user.id
				if not pk: # Проверяем есть ли id задания, если нет отправляем ошибку
						return Response({'error': 'Нет данных о задаче'}, status=status.HTTP_404_NOT_FOUND)
				try: # Пытаемся получить задание, если не удалось - отправляем ошибку
						instance = Task.objects.get(pk=pk)
				except:
						return Response({'error': 'Задача не найдена'}, status=status.HTTP_404_NOT_FOUND)
				if instance.user.id != curr_user: 
						"""
							Проверяем совпадает ли пользователь, который завел задание и пользователь, 
							который отправли запрос, если нет - отправляем ошибку
						"""
						return Response({"error": "Нет доступа к данной задаче."}, status=status.HTTP_403_FORBIDDEN)

				serializer = TaskSerializer(instance, data=request.data, partial=True) # Изменяем данны
				serializer.is_valid(raise_exception=True) # Валидируем данные
				serializer.save() # Обновляем запись в БД
				return Response(serializer.data, status=status.HTTP_200_OK)
		
		def delete_task(self, request, *args, **kwargs):
				# Удаляем задание
				pk = kwargs.get('pk', None)
				curr_user = request.user.id
				if not pk:
						return Response({'error': 'Нет данных о задаче'}, status=status.HTTP_404_NOT_FOUND)
				try:
						instance = Task.objects.get(pk=pk)
				except:
						return Response({'error': 'Задача не найдена'}, status=status.HTTP_404_NOT_FOUND)
				if instance.user.id != curr_user:
						return Response({"error": "Нет доступа к данной задаче."}, status=status.HTTP_403_FORBIDDEN)
				instance.delete()
				return Response({"msg": "Задача удалена"}, status=status.HTTP_200_OK)
		
		def filter_by_status(self, request):
				# Фильтруем задания
				status_param = request.query_params.get('status')
				if status_param is not None:
						tasks = Task.objects.filter(user=request.user.id, status=status_param == "true")
				else:
						tasks = Task.objects.all()
				serializer = TaskSerializer(tasks, many=True)
				return Response(serializer.data)

class MyTokenObtainPairView(TokenObtainPairView):
	# Метод для получения токенов TODO можно возвращать доп данные о пользователе, если не обходимо
	pass

class MyTokenRefreshView(TokenRefreshView):
	# Метод обновления refresh token
	pass