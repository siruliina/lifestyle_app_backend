from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # Model from Django's built-in authentication system
        fields = ['username', 'password', 'email'] # What data we want to expose
        extra_kwargs = {'password': {'write_only': True}} # Don't expose password in response

    def create(self, validated_data):
        user = User.objects.create_user( # Creates a user with hashed password
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user