FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system libs required by geopandas/shapely/rtree
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin libgdal-dev \
    libgeos-dev \
    proj-bin libproj-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps (requirements file is in repo)
COPY python-backend/requirements.txt /app/python-backend/requirements.txt
RUN pip install --no-cache-dir -r /app/python-backend/requirements.txt

# Copy repo (allows writing to /app/public)
COPY . /app

# Run uvicorn
CMD ["uvicorn", "python-backend.main:app", "--host", "0.0.0.0", "--port", "8000"]