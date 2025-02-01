from django.urls import path, include
from .views import UserViewSet, TaskViewSet, MyTokenObtainPairView, MyTokenRefreshView, LogoutView


urlpatterns = [
		path('users/', UserViewSet.as_view(), name='register'),
    path("get_tasks/", TaskViewSet.as_view({
			"get":"get_tasks"
		}), name="get_tasks"),
    path("create_task/", TaskViewSet.as_view({
			"post":"create_task"
		}), name="create_task"),
		path('update_task/<int:pk>/', TaskViewSet.as_view({
			"put":"update_task"
		}), name="update_task"),
		path('delete_task/<int:pk>/', TaskViewSet.as_view({
			"delete":"delete_task"
		}), name="delete_task"),
    path("filter_by_status/", TaskViewSet.as_view({
			"get":"filter_by_status"
		}), name="filter_by_status"),
		path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]