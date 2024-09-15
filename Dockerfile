
FROM python:3.10


WORKDIR /app


COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 50051

# Comando para correr el servidor gRPC
CMD ["python", "cache_system/grpc_service/cache_service.py"]
