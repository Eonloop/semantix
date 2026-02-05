# Use a slim version of Python
FROM python:3.11-slim
WORKDIR /app

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY ./app ./app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]