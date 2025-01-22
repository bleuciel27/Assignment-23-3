# Django Project Setup 

## Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher

## Step 1: Setup Python Environment
1. Install Python if not already installed
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

## Step 2: Install Dependencies
1. Install project requirements:
```bash
pip install -r requirements.txt
```

## Step 3: PostgreSQL Setup
1. Install PostgreSQL if not already installed
   - Download from: https://www.postgresql.org/download/

2. Create a new database:
```sql
CREATE DATABASE sparta_store;
```

3. copy paste setting.py :
    from INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth", ....

 Update database settings in settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sparta_store',
        'USER': 'your_postgres_username',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
``

## Step 4: Django Setup
1. Run database migrations:
```bash
python manage.py migrate
```

2. Create a superuser (admin account):
```bash
python manage.py createsuperuser
```

3. Collect static files:
```bash
python manage.py collectstatic
```

## Step 5: Running the Server
1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application:
   - Main site: http://localhost:8000/api
   - Admin panel: http://localhost:8000/admin

## Common Issues and Solutions

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify database credentials in settings.py
- Check if database exists: `psql -l`

