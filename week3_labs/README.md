<<<<<<< HEAD
# Week 3 Labs - Flet User Login Application

## Overview
A simple user login application built with Flet framework and MySQL database integration.

## Features
- User authentication with MySQL database
- Secure parameterized SQL queries
- User-friendly dialog messages
- Password reveal functionality
- Comprehensive error handling

## Setup Instructions
1. Install dependencies: `pip install flet mysql-connector-python`
2. Set up MySQL database (see SQL commands below)
3. Update database credentials in `src/db_connection.py`
4. Run the application: `flet run`

## Database Setup
```sql
CREATE DATABASE fletapp;
USE fletapp;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
INSERT INTO users (username, password) VALUES ('testuser', 'password123');
=======
# CCCS 106 Projects 
Application Development and Emerging Technologies 
Academic Year 2025-2026 
ECHO is on.
## Repository Structure 
- week1_labs/ - Environment setup and Python basics 
- week2_labs/ - Git and Flet GUI development 
- module1_final/ - Module 1 final project 
>>>>>>> f2befe2ae54a47329aca924ea0e9fcd5a6929858
