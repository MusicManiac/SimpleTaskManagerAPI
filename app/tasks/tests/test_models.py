import pytest
from django.contrib.auth.models import User
from tasks.models import Task

@pytest.mark.django_db
def test_task_creation():
    user = User.objects.create(username='testuser')
    task = Task.objects.create(
        name='Test Task',
        description='This is a test task.',
        status='new',
        assigned_user=user
    )

    assert task.name == 'Test Task'
    assert task.description == 'This is a test task.'
    assert task.status == 'new'
    assert task.assigned_user == user

@pytest.mark.django_db
def test_without_status_creation():
    user = User.objects.create(username='testuser')
    task = Task.objects.create(
        name='Test Task',
        description='This is a test task.',
        assigned_user=user
    )

    assert task.status == 'new'
    assert task.name == 'Test Task'
    assert task.description == 'This is a test task.'
    assert task.assigned_user == user