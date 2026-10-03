FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema y librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación, dashboard y datos evaluados
COPY app.py .
COPY dashboard.py .
COPY cartera_evaluada_powerbi.csv .

# Exponer puertos de FastAPI (8000) y Streamlit (8501)
EXPOSE 8000 8501

# Comando de inicio del microservicio
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]