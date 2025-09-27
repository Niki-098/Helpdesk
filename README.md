# Helpdesk & Ticket Management System

A Django REST Framework-based Helpdesk and Ticketing API with role-based access (User, Agent, Admin), JWT authentication, and task scheduling using Celery.

## Features

User registration & JWT authentication<br>
Role-based permissions (User, Agent, Admin)<br>
Create, assign, update, escalate tickets<br>
Add ticket comments<br>
Reporting API<br>

## API documentation via Swagger/OpenAPI

### Asynchronous background tasks with Celery

**Setup Instructions**
1. Clone the repo<br>
git clone <your-repo-url><br><br>

2. Create and activate a virtual environment<br>
python -m venv venv<br>
**Windows**<br>
venv\Scripts\activate<br>
**Linux/Mac**<br>
source venv/bin/activate<br><br>

3. Install dependencies<br>
pip install -r requirements.txt<br><br>

4. Configure environment variables<br>

Create a .env file in the project root with:<br>

URL_DATABASE=""<br>


## Make sure PostgreSQL and Redis are running.
You can manage PostgreSQL with pgAdmin.<br><br>

5. Apply database migrations<br>
python manage.py migrate<br><br>

6. Create a superuser (Admin)<br>
python manage.py createsuperuser<br>


Then set their role to ADMIN (either via Django shell or automatic logic in CustomUserManager).<br><br>

7. Run the Django server<br>
python manage.py runserver<br><br>


**Visit API docs:** http://127.0.0.1:8000/api/docs/<br>
**Swagger UI →** http://127.0.0.1:8000/api/docs/<br>
**OpenAPI Schema →** http://127.0.0.1:8000/api/schema/<br>

### Testing the APIs

**Register a user →** POST /api/auth/register/<br>
**Login →** POST /api/auth/login/ → copy access token<br>


#### Authorize in Swagger (top-right) → paste token as 

Bearer <your_access_token>


#### Test role-specific APIs:

**User →** Create tickets<br>
**Admin →** Assign, delete, reporting<br>
**Agent →** Update ticket status, add comments<br>

## Tech Stack

**Backend:** Django, Django REST Framework<br>
**Database:** PostgreSQL<br>
**Cache/Tasks:** Redis + Celery<br>
**Auth:** JWT (djangorestframework-simplejwt)<br>
**Docs:** drf-spectacular (Swagger/OpenAPI)<br>

With this setup, anyone can clone, install, migrate, and run the Helpdesk system in minutes.

