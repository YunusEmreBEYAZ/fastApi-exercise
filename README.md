# PyBooking

PyBooking is a backend application for a booking system developed using FastAPI. This project provides a basic API for hotel and room reservation management.

## Features

- User management

- Hotel and room reservation management

- Exception handling for error management

- Database management

## Requirements

To run this project, the following tools and libraries must be installed on your system:

- Python 3.9+

- Virtualenv or any other virtual environment manager

- SQLite (or another supported database)

- FastAPI

- Uvicorn

## Installation

### 1. Clone the Repository

Clone the project to your local machine:

    git clone <repository-url>
    cd PyBooking

### 2. Create a Virtual Environment

Create a virtual environment to run the project in isolation:

    python -m venv fastapi-venv

### 3. Activate the Virtual Environment

Windows:

    fastapi-venv\Scripts\activate

macOS/Linux:

    source fastapi-venv/bin/activate

### 4. Install Dependencies

Install project dependencies using the following command:

    pip install -r requirements.txt

## Database Setup

To set up the database using SQLite, follow these steps:

The data.py file already contains functions to generate dummy data. These functions will run automatically when the server starts.

If you want to initialize the database manually:

    from src.db import database

    database.create_dummy_bookings()

## Running the Application

To start the application, follow these steps:

Make sure you are in the root directory of the project.

Start the server using the following command:

    uvicorn src.main:app --reload

Server URL:

    By default, the application will run at http://127.0.0.1:8000.

API Documentation:

FastAPI provides automatic documentation at the following endpoints:

    Swagger UI: http://127.0.0.1:8000/docs

    ReDoc: http://127.0.0.1:8000/redoc

## Project Structure

````plaintext

src/
├── auth/                 # Authentication module
├── booking/              # Booking operations
│   ├── controller.py     # Controller layer
│   ├── dto.py            # Data transfer objects
│   ├── exceptions.py     # Exception handling
│   ├── mapper.py         # Data mappers
│   ├── repository.py     # Repository layer
│   ├── service.py        # Service layer
├── db/                   # Database connection and models
│   ├── database.py       # Database connection details
│   ├── models.py         # ORM models
├── exception/            # General exception handling
├── router/               # Application routers
├── data.py               # Dummy data creation script
├── main.py               # Application entry point
