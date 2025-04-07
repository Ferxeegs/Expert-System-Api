# Base image dengan Python
FROM python:3.10-slim

# Set working directory dalam container
WORKDIR /app

# Salin semua file ke container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Port yang digunakan Flask
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["python", "main.py"]
