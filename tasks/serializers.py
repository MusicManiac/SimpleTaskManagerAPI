from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class TaskSerializer(serializers.ModelSerializer): # DRF automatically will create fields based on our model
    class Meta:
        model = Task
        fields = '__all__'


class HistoricalTaskSerializer(serializers.ModelSerializer): # handling the task's historical records
    changed_by = serializers.StringRelatedField()

    class Meta:
        model = Task.history.model  # reference to the historical model
        fields = ['id', 'name', 'description', 'status', 'assigned_user', 'history_date', 'history_type', 'changed_by']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user