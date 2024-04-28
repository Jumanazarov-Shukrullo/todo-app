from django.urls import path

from todos.viewsets import TodoAPIView, TodoListAPIView
from .viewsets import RegisterView, LoginView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('todo/all/', TodoListAPIView.as_view(), name='todo-list'),
    path('todo/create/', TodoAPIView.as_view(), name='todo-create'),
    path('todo/<int:pk>/', TodoAPIView.as_view(), name='todo-put'),
]
