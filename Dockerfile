#FROM python:3.13-slim
#
## Install pipenv
#RUN pip install pipenv
#
## Set working directory
#WORKDIR /app
#
## Copy Pipfile and Pipfile.lock
#COPY Pipfile Pipfile.lock ./
#
## Install dependencies
#RUN pipenv install --deploy --system
#
## Copy application code
#COPY app .
#
## Copy Alembic files
#COPY alembic.ini ./
#COPY alembic/ ./alembic/
#
#EXPOSE 8000
#
## Run the application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.13-slim

# Install pipenv
RUN pip install pipenv

# Set working directory
WORKDIR /app

# Copy Pipfile first for caching
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --system

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

EXPOSE 8000

# Set Python path for Alembic imports
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
