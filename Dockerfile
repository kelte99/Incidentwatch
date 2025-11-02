# 1. Imagen base oficial de Python ligera
FROM python:3.13-slim

# 2. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos solo las dependencias primero (mejora cache en builds)
COPY requirements.txt /app/requirements.txt

# 4. Instalamos dependencias en la imagen
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el código de la aplicación dentro de la imagen
COPY app /app/app

# 6. Exponemos el puerto 8000 (puerto interno del contenedor)
EXPOSE 8000

# 7. Comando para arrancar FastAPI con Uvicorn dentro del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
