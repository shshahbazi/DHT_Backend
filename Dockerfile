# Pull base image
FROM python:3.11.5-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=core.production

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . /code/

# Expose port 8000 for Django
#EXPOSE 8000

# Run migrations and start server (only for development, for production use different command)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]