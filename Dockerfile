# Usa una imagen base de Python
FROM python:3.9

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y luego instala las dependencias
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación
COPY app/ .

# Expone el puerto en el que la aplicación Flask se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
