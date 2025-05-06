FROM python:3.11

# Install system dependencies for PyQt6
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pyqt6 \
    libx11-6 libxext6 libxrender1 libxcb1 libxcb-cursor0 \
    libgl1-mesa-glx libegl1-mesa libgl1-mesa-dri \
    libxkbcommon0 libglib2.0-0 x11-apps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Entry point
CMD ["python", "app.py"]
