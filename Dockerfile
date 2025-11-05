FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY online_forum/requirements.txt .
RUN uv pip install -r requirements.txt --system

COPY online_forum/ .

RUN echo '{"name":"online-forum","version":"1.0.0","devDependencies":{"tailwindcss":"^3.4.0"}}' > package.json

RUN npm install

RUN npx tailwindcss init

RUN mkdir -p static_src static/css

RUN echo '@tailwind base;' > static_src/input.css && \
    echo '@tailwind components;' >> static_src/input.css && \
    echo '@tailwind utilities;' >> static_src/input.css

RUN npx tailwindcss -i ./static_src/input.css -o ./static/css/output.css --minify

ENV SECRET_KEY=${SECRET_KEY}

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]

CMD ["sh", "-c", "gunicorn online_forum.wsgi:application --bind 0.0.0.0:$PORT"]