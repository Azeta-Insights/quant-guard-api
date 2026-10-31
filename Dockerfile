FROM python:3.11-slim

# DevSecOps Best Practice: Create a non-root user so the app never runs as admin
RUN groupadd -r quantgroup && useradd -r -g quantgroup quantuser

WORKDIR /app

# Install dependencies first (caches layers to speed up CI/CD)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and hand ownership to our non-root user
COPY main.py .
RUN chown -R quantuser:quantgroup /app

# Switch from root to the restricted user
USER quantuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]