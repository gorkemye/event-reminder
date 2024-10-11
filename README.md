# Event Reminder API

## Overview

The **Event Reminder API** is a RESTful backend service built using Django and Django REST Framework. This API allows
users to create, manage, and retrieve reminders for upcoming events. It supports CRUD operations, event categorization,
and provides endpoints to retrieve upcoming events within the next 24 hours.

### Features

- **Event Management**: Create, read, update, and delete event reminders.
- **Upcoming Events**: Retrieve events happening in the next 24 hours.
- **Categorization**: Filter events by category.
- **Personalized Reminder Timings**: Retrieve personalized reminder times for events.
- **Proxy Models**: Separate proxy model for managing upcoming events only.
- **Automatic Fixture Creation**: A management command to generate 50 random events within the next 10 days.

## Setup and Installation Instructions

### Prerequisites

- Python 3.13+
- Django 5.12+
- Virtual environment

### Installation Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/gorkemye/event-reminder.git
    cd event-reminder-api
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Start the Server**:
    ```bash
    python manage.py runserver
    ```

The API will be accessible at `http://127.0.0.1:8000/api/`.

### Create Sample Data

To populate the database with 50 random events within the next 10 days, run the custom management command:

```bash
python manage.py create_random_events
```

This command will generate random event data that you can use to test the API endpoints.

## API Endpoint Documentation

### 1. Create a New Event

- **Endpoint**: `/api/events/`
- **Method**: `POST`
- **Request Payload**:
    ```json
    {
        "event_title": "Rock Concert",
        "event_description": "Live rock concert featuring local bands.",
        "event_date": "2024-10-15",
        "event_time": "19:00:00",
        "event_category": "Concert",
        "event_reminder_time": "18:30:00"
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "event_title": "Rock Concert",
        "event_description": "Live rock concert featuring local bands.",
        "event_date": "2024-10-15",
        "event_time": "19:00:00",
        "event_category": "Concert",
        "event_reminder_time": "18:30:00",
        "created_at": "2024-10-10T12:00:00Z",
        "updated_at": "2024-10-10T12:00:00Z"
    }
    ```

### 2. Retrieve All Events

- **Endpoint**: `/api/events/`
- **Method**: `GET`
- **Response**:
    ```json
    [
        {
            "id": 1,
            "event_title": "Rock Concert",
            "event_description": "Live rock concert featuring local bands.",
            "event_date": "2024-10-15",
            "event_time": "19:00:00",
            "event_category": "Concert",
            "event_reminder_time": "18:30:00",
            "created_at": "2024-10-10T12:00:00Z",
            "updated_at": "2024-10-10T12:00:00Z"
        },
        ...
    ]
    ```

### 3. Retrieve a Specific Event

- **Endpoint**: `/api/events/{id}/`
- **Method**: `GET`
- **Example**: `/api/events/1/`
- **Response**:
    ```json
    {
        "id": 1,
        "event_title": "Rock Concert",
        "event_description": "Live rock concert featuring local bands.",
        "event_date": "2024-10-15",
        "event_time": "19:00:00",
        "event_category": "Concert",
        "event_reminder_time": "18:30:00",
        "created_at": "2024-10-10T12:00:00Z",
        "updated_at": "2024-10-10T12:00:00Z"
    }
    ```

### 4. Update an Existing Event

- **Endpoint**: `/api/events/{id}/`
- **Method**: `PUT`
- **Request Payload**:
    ```json
    {
        "event_title": "Updated Concert",
        "event_description": "Updated description for the concert.",
        "event_date": "2024-10-16",
        "event_time": "20:00:00",
        "event_category": "Entertainment",
        "event_reminder_time": "19:30:00"
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "event_title": "Updated Concert",
        "event_description": "Updated description for the concert.",
        "event_date": "2024-10-16",
        "event_time": "20:00:00",
        "event_category": "Entertainment",
        "event_reminder_time": "19:30:00",
        "created_at": "2024-10-10T12:00:00Z",
        "updated_at": "2024-10-10T12:30:00Z"
    }
    ```

### 5. Delete an Event

- **Endpoint**: `/api/events/{id}/`
- **Method**: `DELETE`
- **Example**: `/api/events/1/`
- **Response**: `204 No Content`

### 6. Retrieve Upcoming Events

- **Endpoint**: `/api/events/upcoming/`
- **Example**: `/api/events/upcoming/?next_hours=24`
- **Method**: `GET`
- **Default**:`24 Hours`
- **Param**:`next_hours`(int)
    ```json
    [
        {
            "id": 2,
            "event_title": "Doctor Appointment",
            "event_description": "Regular health checkup appointment.",
            "event_date": "2024-10-11",
            "event_time": "14:00:00",
            "event_category": "Health",
            "event_reminder_time": "13:30:00",
            "created_at": "2024-10-10T12:00:00Z",
            "updated_at": "2024-10-10T12:00:00Z"
        }
    ]
    ```

### 7. Retrieve Events by Category

- **Endpoint**: `/api/events/category/{category_name}`
- **Method**: `GET`
- **Example**: `/api/events/category/Concert`
- **Response**:
    ```json
    [
        {
            "id": 1,
            "event_title": "Rock Concert",
            "event_description": "Live rock concert featuring local bands.",
            "event_date": "2024-10-15",
            "event_time": "19:00:00",
            "event_category": "Concert",
            "event_reminder_time": "18:30:00",
            "created_at": "2024-10-10T12:00:00Z",
            "updated_at": "2024-10-10T12:00:00Z"
        }
    ]
    ```

### 8. Retrieve Reminder Time for a Specific Event

- **Endpoint**: `/api/events/{id}/reminder/`
- **Method**: `GET`
- **Example**: `/api/events/1/reminder/`
- **Response**:
    ```json
    {
        "reminder_time": "18:30:00"
    }
    ```

## Sample Queries

Here are some sample cURL commands to interact with the API endpoints:

### Create a New Event

```bash
curl -X POST http://localhost:8000/api/events/ -H "Content-Type: application/json" -d '{
  "event_title": "Music Festival",
  "event_description": "An exciting music festival with multiple bands.",
  "event_date": "2024-10-17",
  "event_time": "18:00:00",
  "event_category": "Concert",
  "event_reminder_time": "17:30:00"
}'
```

### Get All Events

```bash
curl -X GET http://localhost:8000/api/events/
```

### Get Events by Category

```bash
curl -X GET http://localhost:8000/api/events/category/Concert/
```

### Get Upcoming Events

```bash
curl -X GET http://localhost:8000/api/events/upcoming/
```

### Get Reminder Time for a Specific Event

```bash
curl -X GET http://localhost:8000/api/events/1/reminder/
```

## Postman Collection Import

To facilitate testing of the API, a Postman collection file has been included in the repository. You can find the
Postman collection file at the following location:

```
PycharmProjects\event-reminder\postman_collection.json
```

## API Documentation with Swagger and Redoc

The project includes integrated API documentation using **Swagger** and **Redoc**. You can access these interactive API
documentation pages to explore and test the API endpoints.

### Accessing Swagger Documentation

- **Swagger URL**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Swagger provides an interactive interface where you can test all the API endpoints, view request and response formats,
  and interact with the API directly from the browser.

### Accessing Redoc Documentation

- **Redoc URL**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- Redoc provides a user-friendly API documentation page with a clean and easy-to-read interface.
