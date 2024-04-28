from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from todos.models import Todo
from todos.serializers import TodoSerializer


class CustomPermission(IsAuthenticated):
    def has_permission(self, request, view):
        """
            Check if the user has permission to perform the requested action.
            Args:
                request: HTTP request object.
                view: View object for which permission is being checked.
            Returns:
                bool: True if the user has permission, False otherwise.
        """
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True


class TodoListAPIView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
            Get the queryset of todos.
            Returns:
            queryset: Queryset of todos.
        """
        queryset = Todo.objects.all()
        return queryset

    def get_serializer_context(self):
        """
            Get the context for the serializer.
            Returns:
                dict: Context for the serializer.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TodoAPIView(APIView):
    permission_classes = [CustomPermission, ]

    def post(self, request):
        """
            Handle POST requests for creating a todo.
            Args:
                request: HTTP request object containing todo data.
            Returns:
                Response: HTTP response with todo data and status code.
        """
        serializer = TodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
            Handle PUT requests for updating a todo.
            Args:
                request: HTTP request object containing updated todo data.
                args: Additional positional arguments.
                kwargs: Additional keyword arguments.
            Returns:
                Response: HTTP response with updated todo data and status code.
        """
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Todo.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        if instance.created_at >= timezone.now() - timedelta(days=1):
            serializer = TodoSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Todo can only be updated within 24 hours of creation'},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
            Handle DELETE requests for deleting a todo.
            Args:
                request: HTTP request object.
                args: Additional positional arguments.
                kwargs: Additional keyword arguments.
            Returns:
                Response: HTTP response with status code indicating success or failure.
        """
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()

        return Response({"post": "delete todo " + str(pk)}, status=status.HTTP_204_NO_CONTENT)
