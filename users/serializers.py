# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'user_email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use our custom create_user to handle password hashing
        return User.objects.create_user(
            user_email=validated_data['user_email'],
            user_name=validated_data.get('user_name', ''),
            password=validated_data['password']
        )