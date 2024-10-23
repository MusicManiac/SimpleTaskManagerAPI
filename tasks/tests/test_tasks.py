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
        self.user_2 = User.objects.create(username='chef')
        self.tasks = [
            Task.objects.create(
                name='Test Task 1',
                description='This is the first test task.',
                status='new',
                assigned_user=self.user
            ),
            Task.objects.create(
                name='Test Task 2',
                description='This is the second test task.',
                status='in_progress',
                assigned_user=self.user
            ),
            Task.objects.create(
                name='Cooking',
                description='Cook some soup',
                status='finished',
                assigned_user=self.user_2
            )
        ]

    def test_create_new_task(self):
        data = {
            'name': 'New Task',
            'description': 'Description of new task',
            'status': 'new',
            'assigned_user': self.user.id
        }
        response = self.client.post(reverse('task-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 4  # Make sure there are now 4 tasks
        assert Task.objects.get(id=response.data['id']).name == 'New Task'

    def test_get_task_list(self):
        response = self.client.get(reverse('task-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # Check if we get the initial tasks

    def test_filter_task_by_status(self):
        response = self.client.get(reverse('task-list'), {'status': 'new'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Should return the test task

    def test_filter_task_by_partial_name(self):
        response = self.client.get(reverse('task-list'), {'name': 'Task'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_filter_task_by_partial_description(self):
        response = self.client.get(reverse('task-list'), {'description': 'soup'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_filter_task_by_partial_description_2(self):
        response = self.client.get(reverse('task-list'), {'description': 'this will return 0 hits'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_filter_task_by_user(self):
        response = self.client.get(reverse('task-list'), {'assigned_user': self.user.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_task_history(self):
        response = self.client.get(reverse('task-detail', args=[self.tasks[0].id]) + 'history/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0  # History is recorded

    def test_edit_task(self):
        updated_data = {
            'name': 'Updated Task Name',
            'description': 'This is an updated description.',
            'status': 'in_progress',
            'assigned_user': self.user.id
        }

        response = self.client.put(reverse('task-detail', args=[self.tasks[0].id]), updated_data)

        assert response.status_code == status.HTTP_200_OK
        updated_task = Task.objects.get(id=self.tasks[0].id)

        assert updated_task.name == updated_data['name']
        assert updated_task.description == updated_data['description']
        assert updated_task.status == updated_data['status']
        assert updated_task.assigned_user.id == updated_data['assigned_user']

    def test_edit_task_without_name(self):
        updated_data = {
            'name': '',  # Leaving name empty
            'description': 'This should fail.',
            'status': 'in_progress',
            'assigned_user': self.user.id
        }

        response = self.client.put(reverse('task-detail', args=[self.tasks[1].id]), updated_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST