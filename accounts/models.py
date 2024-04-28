from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# Custom user manager for handling user creation
class MyUserManager(BaseUserManager):
    # Method for creating a regular user
    def create_user(self, username, password=None, **kwargs):
        if username is None:
            raise TypeError('Users must have username')
        if password is None:
            raise TypeError('Users must have password')
        # Create a new user object with provided username and other optional fields
        user = self.model(username=username, **kwargs)
        user.set_password(password)  # Set the password using Django's hashing mechanism
        user.save(using=self._db)  # Save the user to the database using the default database
        return user

    # Method for creating a superuser with administrative privileges
    def create_superuser(self, username, password=None, **kwargs):
        if username is None:
            raise TypeError('Superusers must have username')
        if password is None:
            raise TypeError('Superusers must have password')
        # Create a regular user first
        user = self.create_user(
            username,
            password=password,
            **kwargs
        )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Custom user model based on AbstractBaseUser
class User(AbstractBaseUser):
    # Username field
    username = models.CharField(db_index=True, max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    # Whether the user has superuser privileges
    is_superuser = models.BooleanField(default=False, null=True, blank=True)
    # Timestamps for creation and update
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    # Custom user manager

    objects = MyUserManager()
    # Field to use as the unique identifier for authentication
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    # Property to indicate whether the user has staff permissions (required for admin access)
    @property
    def is_staff(self):
        return self.is_superuser
