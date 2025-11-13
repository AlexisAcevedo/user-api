# Etapa 1: Builder
FROM python:3.13-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python en un directorio virtual
RUN pip install --user --no-cache-dir -r requirements.txt


# Etapa 2: Runtime
FROM python:3.13-slim

WORKDIR /app

# Instalar solo dependencias de runtime
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar Python dependencies desde builder
COPY --from=builder /root/.local /root/.local

# Establecer PATH
ENV PATH=/root/.local/bin:$PATH

# Copiar toda la aplicación
COPY . .

# Crear directorio para logs
RUN mkdir -p logs

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Exponer puertos
EXPOSE 8000 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

