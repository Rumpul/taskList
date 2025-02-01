from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=255, verbose_name="Название")
	description = models.TextField(blank=True, null=True, verbose_name="Описание")
	status = models.BooleanField(default=False, verbose_name="Статус (Выполнено/Нет)")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
	due_date = models.DateField(null=True, blank=True, verbose_name="Дата выполнения")

	def __str__(self):
			return self.title

	class Meta:
			verbose_name = "Задача"
			verbose_name_plural = "Задачи"