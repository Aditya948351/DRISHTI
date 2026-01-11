FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN cd DrishtiPlatform && python manage.py collectstatic --no-input

# Run gunicorn
CMD ["sh", "-c", "cd DrishtiPlatform && gunicorn DrishtiPlatform.wsgi:application --bind 0.0.0.0:$PORT"]
