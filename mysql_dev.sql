-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS car_dev_db;
CREATE USER IF NOT EXISTS 'user_dev'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON `car_dev_db`.* TO 'user_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'user_dev'@'localhost';
FLUSH PRIVILEGES;
