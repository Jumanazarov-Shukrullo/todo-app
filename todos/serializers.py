from rest_framework import serializers

from accounts.models import User
from todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """
        Serializer for Todo model.
    """

    # Serializer method field to get the author's username
    author = serializers.SerializerMethodField()
    # Field to accept author ID during input
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        """
            Meta class for TodoSerializer.
        """
        model = Todo
        fields = ['title', 'description', 'author_id', 'author']
        ordering = ['-created_at']

    def create(self, validated_data):
        """
            Method to create a new todo instance.
            Args:
                validated_data (dict): Validated data for todo creation.
            Returns:
                Todo: Created todo instance.
        """
        author_id = validated_data.pop('author_id', None)
        if author_id is not None:
            validated_data['author'] = User.objects.get(pk=author_id)
        return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
            Method to update an existing todo instance.
            Args:
                instance (Todo): Existing todo instance.
                validated_data (dict): Validated data for todo update.
            Returns:
                Todo: Updated todo instance.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        return instance

    def get_author(self, obj):
        """
            Method to get the author's username.
            Args:
                obj (Todo): Todo object.
            Returns:
                str: Author's username or None.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author.username
        return None
