
# Event Reminder API

## Overview

The **Event Reminder API** is a RESTful backend service built using Django and Django REST Framework. This API enables users to create, manage, and retrieve reminders for events. It supports CRUD operations, event categorization, and allows dynamic retrieval of upcoming events for any specified timeframe. It also provides the flexibility to include or exclude canceled events.

### Features

- **Event Management**: Create, read, update, and delete event reminders.
- **Upcoming Events**: Retrieve upcoming events dynamically for any specified timeframe.
- **Categorization**: Filter events by category.
- **Cancel Events**: Soft delete events by marking them as canceled.
- **Personalized Reminder Timings**: Set reminders for events with customizable times.
- **Reminder Note**: Provide personalized reminder notes.
- **Proxy Models**: Manage upcoming, expired, and canceled events with separate models.
- **Automatic Fixture Creation**: Populate the database with random events using a custom management command.

### Endpoints
- **Create Event**: POST `/api/events/`
- **Retrieve All Events**: GET `/api/events/`
- **Retrieve Event by ID**: GET `/api/events/{id}/`
- **Update Event**: PUT `/api/events/{id}/`
- **Delete Event**: DELETE `/api/events/{id}/`
- **Cancel Event**: POST `/api/events/{id}/cancel/`
- **Retrieve Upcoming Events**: GET `/api/events/upcoming/`
- **Retrieve Events by Category**: GET `/api/events/category/{category_name}`
- **Retrieve Reminder Details**: GET `/api/events/{id}/reminder/`
- **Swagger Documentation**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

## Setup and Installation Instructions

### Prerequisites

- Python 3.13+
- Django 5.12+
- Virtual environment

### Installation Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/gorkemye/event-reminder.git
    cd event-reminder
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

The API will be accessible at `http://localhost:8000/api/`

### Create Sample Data

Use the following management command to generate 50 random events for testing:
```bash
python manage.py create_random_events
```

## API Endpoint Documentation

### 1. Create a New Event

**Endpoint**: `/api/events/`  
**Method**: `POST`

Request Payload:
```json
{
        "category": "Finance",
        "title": "Team Building Activity",
        "description": "Improve your guitar skills in this practice session.",
        "event_date": "2024-10-12",
        "event_time": "17:15:00",
        "is_canceled": true,
        "reminder_settings": {
            "reminder_time": "2024-10-12T08:41:00+03:00",
            "notification_methods": [
                "Email"
            ],
            "reminder_note": "Reminder for Team Building Activity"
        }
}
```
Response:
```json
{
    "id": 57,
    "category": "Finance",
    "title": "Team Building Activity",
    "description": "Improve your guitar skills in this practice session.",
    "is_upcoming": true,
    "event_date": "2024-10-12",
    "event_time": "17:15:00",
    "is_canceled": true,
    "reminder_settings": {
        "reminder_time": "2024-10-12T08:41:00+03:00",
        "notification_methods": [
            "Email"
        ],
        "reminder_note": "Reminder for Team Building Activity"
    }
}
```

### 2. Retrieve All Events

**Endpoint**: `/api/events/`  
**Method**: `GET`

### 3. Retrieve Event by ID

**Endpoint**: `/api/events/{id}/`  
**Method**: `GET`

Response:
```json
[
    {
        "id": 46,
        "category": "Finance",
        "title": "Team Building Activity",
        "description": "Improve your guitar skills in this practice session.",
        "is_upcoming": false,
        "event_date": "2024-10-12",
        "event_time": "09:15:00",
        "is_canceled": true,
        "reminder_settings": {
            "reminder_time": "2024-10-12T08:41:00+03:00",
            "notification_methods": [
                "Email"
            ],
            "reminder_note": "Reminder for Team Building Activity"
        }
    }...
]
```

### 4. Update Event

**Endpoint**: `/api/events/{id}/`  
**Method**: `PUT`

Request Payload:
```json
{
    "category": "Personal",
    "title": "Updated Event",
    "description": "Updated description.",
    "event_date": "2024-10-21",
    "event_time": "15:00:00",
    "reminder_settings": {
        "reminder_time": "2024-10-21T14:30:00",
        "notification_methods": ["Email"],
        "reminder_note": "Updated reminder note."
    }
}
```

### 5. Delete Event

**Endpoint**: `/api/events/{id}/`  
**Method**: `DELETE`

**Example**: `localhost:8000/api/events/1/`

Response:
```json
{"detail":"Event successfully deleted."}
```
Exception:
```json
{"detail":"No Event matches the given query."}
```


### 6. Cancel Event

**Endpoint**: `/api/events/{id}/cancel/`  
**Method**: `POST`

Response:
```json
{"detail":"Event successfully canceled."}
```
Exception:
```json
{"detail":"This event is already canceled."}
```

### 7. Retrieve Upcoming Events

**Endpoint**: `/api/events/upcoming/`  
**Method**: `GET`  

Query Parameters:
- **next_hours**: Integer, timeframe in hours (default: 24)
- **show_canceled**: Boolean, whether to include canceled events (default: false)
- **category**: String, filter by event category (optional)

Example Request:
```bash
localhost:8000/api/events/upcoming?next_hours=24&show_canceled=true&category=Work
```

### 8. Retrieve Events by Category

**Endpoint**: `/api/events/category/{category_name}`  
**Method**: `GET`

### 9. Retrieve Reminder Details

**Endpoint**: `/api/events/{id}/reminder/`  
**Method**: `GET`

**Example Request**: `localhost:8000/api/events/1/reminder/`

Response:
```json
{
    "event_id": 2,
    "event_title": "Project Planning",
    "reminder_time": "2024-10-17T08:22:00Z",
    "notification_methods": [
        "Email",
        "SMS"
    ],
    "reminder_note": "Reminder for Project Planning"
}
```

## API Documentation with Swagger and Redoc

Access the interactive API documentation:

- **Swagger**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Postman Collection

The Postman collection file is available for import at:

```
PycharmProjects/event-reminder/postman_collection.json
```
