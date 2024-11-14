CREATE USER task_admin WITH PASSWORD 'admin';
CREATE DATABASE task_manager;
ALTER USER task_admin CREATEDB;
GRANT ALL ON SCHEMA public TO task_admin;
GRANT ALL PRIVILEGES ON DATABASE task_manager TO task_admin;
ALTER DATABASE task_manager OWNER TO task_admin;