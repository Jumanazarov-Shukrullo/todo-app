from django.db import models

from accounts.models import User


class Todo(models.Model):
    """
        Model for Todo items.
    """
    # Title of the todo
    title = models.CharField(max_length=255)
    # Description of the todo
    description = models.TextField()
    # Flag indicating whether the todo is completed or not
    done = models.BooleanField(default=False)
    # Date and time when the todo was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Date and time when the todo was last updated
    updated_at = models.DateTimeField(auto_now=True)
    # User who created the todo
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
