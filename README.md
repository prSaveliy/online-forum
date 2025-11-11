# Online Forum Django Application

An interactive and **adaptive** online forum built with **Django**, **Tailwind CSS**, **PostgreSQL**, and **Docker**. This application allows users to create, explore, and interact with posts using tags, likes, comments, and more.

---

## Features

- Users can **create posts** that appear on the **feed page** and their **profile page**.  
- Posts can be **tagged**, similar to hashtags. Clicking a tag shows all posts with that tag.  
- Users can **like**, **comment**, and **share posts via email**.  
- **Search functionality** powered by PostgreSQL allows users to find posts quickly.  
- **Adaptive and responsive design** using **Tailwind CSS**, works seamlessly on mobile, tablet, and desktop.  
- Dockerized setup for easy deployment.

---

## Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML + Tailwind CSS  
- **Database:** PostgreSQL  
- **Containerization:** Docker  
- **Languages:** Python, HTML  

---

## Installation

You can set up the project either **with Docker** or **manually**.

### Option 1: Using Docker (Recommended)

1. **Clone the repository:**

```bash
git clone https://github.com/prSaveliy/online-forum.git
cd online_forum
```

2. **Create a .env in your root directory and set environment variables:**

```.env
DEBUG=True
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=forum <your_email>
ALLOWED_HOSTS=localhost
SECRET_KEY=your_secret_key
```
to get django secret key use third-party services to generate the key for you

```bash
# uncomment this databases setting in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
}
# and comment out this one:
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'), conn_max_age=600, ssl_require=True)
}
# also change npm_bin path if you chose custom installation path
# or if you are not on Windows
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

3. **Build and run Docker containers:**

```bash
docker-compose up --build
```

4. **Apply Django migrations:**

```bash
docker-compose exec web python manage.py migrate
```

5. **Create a superuser (optional):**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access the application at http://localhost:8000

### Option 2: Manual Setup

1. **Clone the repository:**

```bash
git clone https://github.com/prSaveliy/online-forum.git
cd online_forum
```

2. **Create a virtual environment and activate it:**

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Mac/Linux
source .venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create a .env in your root directory and set environment variables:**

```.env
DEBUG=True
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=forum <your_email>
ALLOWED_HOSTS=localhost
SECRET_KEY=your_secret_key
```
to get django secret key use third-party services to generate the key for you

```bash
# uncomment this databases setting in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
}
# and comment out this one:
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'), conn_max_age=600, ssl_require=True)
}
# also change npm_bin path if you chose custom installation path
# or if you are not on Windows
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

5. **Apply Django migrations:**

```bash
python manage.py migrate
```

6. **Create a superuser (optional):**

```bash
python manage.py createsuperuser
```

7. **Start the development server:**

```bash
python manage.py runserver
```



