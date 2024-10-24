# Task Manager API
This is my introductory project to Django, demonstrating how to build a RESTful API for managing tasks.

A Django-based API for managing tasks, allowing users to create, update, delete, and filter tasks. The API also tracks the history of task changes.

## Features

- Create, retrieve, update, and delete tasks.
- Filter tasks by status, name, and assigned user.
- Track task history.
- User registration.

## Technologies and Packages Used

- [Python 3.12.7](https://www.python.org/downloads/)
- [Django](https://www.djangoproject.com/download/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [django-simple-history](https://django-simple-history.readthedocs.io/en/latest/)
- [django_filters](https://django-filter.readthedocs.io/en/stable/)
- [pytest](https://docs.pytest.org/en/stable/) for testing

## Installation
Ensure you have the following installed:

- [Python 3.12.7 or newer](https://www.python.org/downloads/) (few versions behind probably would also work)
- [PostgreSQL](https://www.postgresql.org/download/)
- [pip](https://pip.pypa.io/en/stable/)
- Installation process is described presuming using [PyCharm Community](https://www.jetbrains.com/pycharm/download/), may vary with other IDEs

### Steps

Setting up PSQL:
1. Open SQL shell (psql),
2. Log in as superuser
3. Setup initial database by running following commands in SQL shell (psql):
   ```
   CREATE USER task_admin WITH PASSWORD 'admin';
   CREATE DATABASE task_manager;
   ALTER USER task_admin CREATEDB;
   GRANT ALL ON SCHEMA public TO task_admin;
   GRANT ALL PRIVILEGES ON DATABASE task_manager TO task_admin;
   ALTER DATABASE task_manager OWNER TO task_admin;
   ```
4. Later on you can delete traces of this repo by running following commands in psql:
   ```
   DROP DATABASE task_manager;
   REVOKE ALL ON SCHEMA public FROM task_admin;
   DROP USER task_admin;
   ```

Setting up project:
1. Clone repo
2. Setup Python Interpreter (PyCharm will complain that project does not have one set up, proceed to project settings and setup your previously installed Python there as interpreter)
3. Open terminal, make sure you're in virtual enviroment (.venv) and install required packages:
   ```
   python -m pip install --upgrade pip
   pip install Django djangorestframework psycopg2-binary django-filter django-simple-history pytest pytest-django
   ```
4. Make migrations and import provided initial data
   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py loaddata tasks/fixtures/initial_data_with_history.json
   ```
5. Run the server with `python manage.py runserver`

## Tests
Testing is implemented using [pytest](https://docs.pytest.org/en/stable/) and can be done by running command `pytest` in your virtual enviroment
![image](https://github.com/user-attachments/assets/20170793-6230-46e1-9bfe-5c3b7a60ad92)


## Usage
You can interact with API usng cURLs and/or browser

Tasks API Endpoints

| Method | Endpoint | Description |
| ------------- | ------------- | ------------- |
| GET  | /api/tasks/ | List all tasks |
| POST  | /api/tasks/ | Create a new task |
| GET  | /api/tasks/{id}/ | Get a task by ID |
| PUT  | /api/tasks/{id}/ | Update a task |
| DELETE  | /api/tasks/{id}/ | Delete a task |
| GET  | /api/tasks/{id}/history/ | Get the history of a task |

Users API Endpoints

| Method | Endpoint | Description |
| ------------- | ------------- | ------------- |
| GET  | /api/users/ | List all users |
| POST  | /api/users/ | Create a new user |
| GET  | /api/users/{id}/ | Get a user by ID |
| PUT  | /api/users/{id}/ | Update a user |
| DELETE  | /api/users/{id}/ | Delete a user |

### Examples:
> [!NOTE]
> When using windows command line, remember that you have to replace `"` with `\"` inside double quotes when sending json over so it's parsed corectly, as example:<br />
> `curl -X POST http://127.0.0.1:8000/api/tasks/ -H "Content-Type: application/json" -d "{"name": "CLI Task", "description": "Task created via curl", "status": "new"}"`<br />
> becomes<br />
> `curl -X POST http://127.0.0.1:8000/api/tasks/ -H "Content-Type: application/json" -d "{\"name\": \"CLI Task\", \"description\": \"Task created via curl\", \"status\": \"new\"}"`

Format:
```
curl

response
```
List of tasks:
```
curl -X GET http://127.0.0.1:8000/api/tasks/

[{"id":1,"name":"Test Task 1","description":"Description here","status":"in_progress","assigned_user":1},{"id":2,"name":"Task 2","description":"Description 2","status":"new","assigned_user":1}]
```
Filter tasks with status "New"
```
curl -X GET http://127.0.0.1:8000/api/tasks/?status=new

[{"id":2,"name":"Task 2","description":"Description 2","status":"new","assigned_user":1}]
```
Add new task
```
curl -X POST http://127.0.0.1:8000/api/tasks/ -H "Content-Type: application/json" -d "{\"name\": \"CLI Task\", \"description\": \"Task created via curl\", \"status\": \"new\"}"

{"id":3,"name":"CLI Task","description":"Task created via curl","status":"new","assigned_user":null}
```
Edit a task
```
curl -X PUT http://127.0.0.1:8000/api/tasks/3/ -H "Content-Type: application/json" -d "{\"name\": \"CLI Task\", \"description\": \"Task edited via curl\", \"status\": \"in_progress\"}"

{"id":3,"name":"CLI Task","description":"Task edited via curl","status":"in_progress","assigned_user":null}
```
View history of a task
```
curl -X GET http://127.0.0.1:8000/api/tasks/3/history/

[{"id":3,"name":"CLI Task","description":"Task edited via curl","status":"in_progress","assigned_user":null,"history_date":"2024-10-23T19:03:15.710752Z","history_type":"~"},{"id":3,"name":"CLI Task","description":"Task created via curl","status":"new","assigned_user":null,"history_date":"2024-10-23T18:55:42.357661Z","history_type":"+"}]
```
Add new user
```
curl -X POST http://127.0.0.1:8000/api/users/ -H "Content-Type: application/json" -d "{\"username\": \"newuser\", \"password\": \"newpassword123\", \"email\": \"newuser@example.com\", \"first_name\": \"New\", \"last_name\": \"User\"}"

{"id":2,"username":"newuser","email":"newuser@example.com","first_name":"New","last_name":"User"}
```
List of users (assuming after adding new user with previous example):
```
curl -X GET http://127.0.0.1:8000/api/users/

[{"id":1,"username":"TestUser","email":"example@gmail.com","first_name":"Test","last_name":"User"},{"id":2,"username":"newuser","email":"newuser@example.com","first_name":"New","last_name":"User"}]
```

All of this is also accessible via browser by opening http://127.0.0.1:8000/api/ with the help of Django REST framework.

https://github.com/user-attachments/assets/e88fcb57-8aeb-4ca9-8284-1aace18ce31f

## License
[MIT](https://github.com/MusicManiac/SimpleTaskManagerAPI/blob/master/LICENSE)
