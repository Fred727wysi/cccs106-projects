Weather Application - Module 6 Lab

Student Information

Name: Frederick D. Ortinero

Student ID: 231002330

Course: CCCS 106

Section: 3A


Project Overview

This project is a cross-platform weather application built with Flet, a Python framework that enables the creation of interactive desktop, mobile, and web apps. The application delivers real-time weather information through a sleek, modern interface, allowing users to conveniently access forecasts for any city.

Weather data and forecasts are retrieved from the OpenWeatherMap API based on user-entered city names. The application features a responsive design and includes practical functionalities such as temperature unit conversion and theme switching.

Implemented Features

1. Search History – Quick access to previously searched cities.


2. Temperature Unit Toggle – Switch between Celsius (°C) and Fahrenheit (°F).


3. Weather Condition Icons & Dynamic Colors – Visual feedback reflecting current weather.


4. 5-Day Weather Forecast – Summary of upcoming weather trends.


5. Dark Mode Support – Comfortable viewing in low-light environments.



Core Features

[✓] Search for cities

[✓] Display current weather

[✓] Show temperature, humidity, and wind speed

[✓] Weather icons representation

[✓] Error handling for invalid inputs

[✓] Modern Material Design-inspired UI


Enhanced Features

1. Search History

Maintains a dropdown of the last 5 successful searches for easy recall, eliminating the need to re-enter city names.



2. Temperature Unit Toggle

Allows users to switch between Celsius and Fahrenheit for both current conditions and forecasts via a simple toggle button.



3. Weather Condition Icons & Dynamic Colors

Changes the background color and displays appropriate weather icons according to the current conditions (e.g., sunny, rainy, snowy), offering intuitive visual cues.



4. 5-Day Weather Forecast

Processes 3-hour interval API data and presents a concise daily summary showing minimum and maximum temperatures for the next five days.




Installation

Prerequisites

Python 3.8 or later

pip package manager


Setup Instructions

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
