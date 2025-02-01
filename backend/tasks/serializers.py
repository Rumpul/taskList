from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
		# Сериалайзер для пользователя
		class Meta:
				model = User
				fields = ['id', 'username', 'password']
				extra_kwargs = {'password': {'write_only': True}}

		def create(self, validated_data):
				user = User.objects.create_user(**validated_data)
				return user

class TaskSerializer(serializers.ModelSerializer):
		# Сериалайзер задач
		class Meta:
				model = Task
				fields = '__all__'