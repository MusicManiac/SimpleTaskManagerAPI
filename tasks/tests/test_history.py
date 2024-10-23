import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from tasks.models import Task

@pytest.mark.django_db
class TestTaskAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.task = Task.objects.create(
            name='Test Task',
            description='This is a test task.',
            status='new',
            assigned_user=self.user
        )

    def test_get_task_history(self):
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_edit_task(self):
        updated_data = {
            'name': 'Updated Task Name',
            'description': 'This is an updated description.',
            'status': 'in_progress',
            'assigned_user': self.user.id
        }
        response = self.client.put(reverse('task-detail', args=[self.task.id]), updated_data)

        assert response.status_code == status.HTTP_200_OK
        updated_task = Task.objects.get(id=self.task.id)

        assert updated_task.name == updated_data['name']
        assert updated_task.description == updated_data['description']
        assert updated_task.status == updated_data['status']
        assert updated_task.assigned_user.id == updated_data['assigned_user']