# syntax=docker/dockerfile:1

#imagen del contenedor (la descarga de dockerhub)
FROM python:3.11.4

#Se situal en el directorio app del contenedor
WORKDIR /app

#Copia el archivo al raiz del contenedor
COPY requirements.txt ./

#Ejecuta un comando en el contenedor
RUN pip install -r requirements.txt

#Copia todo el proyecto en el raiz del contenedor
COPY . .

#Expone un puerto en el contenedor
EXPOSE 5000

#Setea variables de entorno
ENV FLASK_APP=index.py
ENV APP_SETTINGS_MODULE="config.pre"

#Ejecuta el comando flask run --host 0.0.0.0 cuando se inicia el contenedor. 
CMD ["flask", "run", "--host", "0.0.0.0"]
