# Celestius Event Registration API

## Overview
A backend API built with Python, Flask, and SQLite for managing registrations for the Backend Development Workshop on 20 October 2026.

## Features
- Register students with name and email.
- Store optional college and department details.
- Record registration timestamps automatically.
- Limit registrations to 50 participants.
- Prevent duplicate email registrations.
- Retrieve all registrations.
- Retrieve registrations by ID or email.
- Validate input and return appropriate error responses.

## Technologies
- Python
- Flask
- SQLite

## Setup and Run
1. Open the project folder in VS Code.
2. Activate the virtual environment on Windows:

   `.venv\Scripts\activate`

3. Start the application:

   `python app.py`

4. Open `http://127.0.0.1:5000` in your browser.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | View event information |
| POST | `/register` | Register a student |
| GET | `/registrations` | View all registrations |
| GET | `/registrations/<id>` | Find a registration by ID |
| GET | `/registrations/email/<email>` | Find by email |

## Example Registration Request

Send a POST request to `/register` with JSON:

```json
{
  "name": "Test Student",
  "email": "test@example.com",
  "college": "My College",
  "department": "IT"
}
```

## Error Handling
- `400 Bad Request`: Missing or invalid input.
- `404 Not Found`: Registration does not exist.
- `409 Conflict`: Duplicate email or event capacity reached.

## Database
SQLite stores registrations in `registrations.db`, created automatically when the application starts.

## Author
Created as a backend recruitment assignment for Celestius.
