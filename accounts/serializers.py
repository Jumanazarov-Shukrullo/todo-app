from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    # Serializer fields for user model
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        # Define model and fields for serialization
        model = User
        fields = ['id', 'username', 'password', 'created', 'updated', 'is_active']
        # Define extra kwargs for serializer fields
        kwargs_extra = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        # Retrieve the password
        password = validated_data.pop('password', None)
        # Create a new user instance
        instance = self.Meta.model(**validated_data)
        # Set password for the user if provided
        if password is not None:
            try:
                validate_password(password=password)
            except ValidationError as e:
                raise serializers.ValidationError({'password': e.messages})
            instance.set_password(password)
        instance.save()
        return instance
