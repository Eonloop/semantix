# Utilizing a slim version of Python to keep the image small
FROM python:3.13-slim
WORKDIR /app

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY ./app ./app
EXPOSE 8000

# Run the uvicorn web server for the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]