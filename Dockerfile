FROM node:20 AS tailwind-builder

WORKDIR /app/online_forum/theme/static_src

RUN apt-get update && apt-get install -y build-essential

COPY online_forum/theme/static_src/package*.json ./online-forum/theme/static_src/

RUN npm install

WORKDIR /app
COPY . .

WORKDIR /app/online_forum/theme/static_src
RUN npm run build


FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY online_forum/requirements.txt .
RUN uv pip install -r requirements.txt --system

COPY online_forum/ .

COPY --from=tailwind-builder /app/theme/static_src/static/css ./theme/static_src/static/css

RUN python manage.py collectstatic --noinput

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD gunicorn online_forum.wsgi:application --bind 0.0.0.0:$PORT