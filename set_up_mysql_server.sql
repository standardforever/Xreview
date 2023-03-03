-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS XReview;
CREATE USER IF NOT EXISTS "admin"@"localhost" IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON `XReview`.* TO 'admin'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;  