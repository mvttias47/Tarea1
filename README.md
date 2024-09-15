# Proyecto de Sistemas Distribuidos: Sistema de Caché Externo al DNS

## Descripción

Este proyecto implementa un sistema de caché distribuido utilizando Redis para optimizar las consultas DNS. El sistema está compuesto por un cliente gRPC, un servidor gRPC, y un sistema de caché distribuido que utiliza particiones para almacenar las respuestas de las solicitudes de DNS. Se implementan dos políticas de remoción de entradas en el caché: `LRU (Least Recently Used)` y `Random`.

### Funcionalidades

- **Caché Distribuido:** Utiliza Redis como caché distribuido con particionamiento de 2, 4 y 8 particiones.
- **Políticas de Remoción:** Se implementaron las políticas de remoción `LRU` y `Random`.
- **Particionamiento por Hash y por Rango:** El sistema soporta particionamiento de las solicitudes de caché tanto por hash como por rango.
- **Cliente y Servidor gRPC:** Se utilizan servicios gRPC para la comunicación entre el cliente, el servidor y el sistema de caché.
- **Resolución DNS:** Si una consulta no está en caché (MISS), se realiza una resolución DNS utilizando el comando `dig`.
  
## Componentes

- **Cliente gRPC:** Envía solicitudes de resolución de dominios utilizando un dataset de prueba.
- **Servidor gRPC:** Gestiona las solicitudes del cliente, busca en el caché Redis y, si no se encuentra, hace una consulta al DNS usando `dig`.
- **Redis:** Sistema de almacenamiento en caché distribuido, configurado con 2, 4 y 8 particiones.
  
## Requisitos

- **Docker**: Para la ejecución de Redis en múltiples particiones.
- **Docker Compose**: Para la orquestación de contenedores Redis y el servidor gRPC.
- **Python 3.10**: Para ejecutar el cliente y servidor gRPC.
- **Redis 6+**
- **gRPC 1.44.0**
  
### Instalación y Configuración

1. **Clonar el Repositorio:**
   ```bash
   git clone https://github.com/mvttias47/Tarea1.git
   cd Tarea1

### Instalar dependencias

pip install -r requirements.txt

### Redis está configurado para funcionar con múltiples particiones. El siguiente comando levantará los contenedores de Redis:

docker-compose up --build

### El script configurar_redis.sh está configurado para aplicar las políticas de LRU o Random a todas las particiones de Redis.

bash configurar_redis.sh

### Para iniciar el servidor gRPC, que actúa como intermediario entre las solicitudes del cliente y el sistema de caché:

python cache_system/grpc_service/cache_service.py

### El cliente genera tráfico de solicitudes de resolución de nombres basadas en un dataset. Para ejecutarlo:

python cache_system/grpc_service/client.py

Autores
Matías Muñoz
Benjamín Salinas

Este proyecto fue desarrollado como parte de la asignatura Sistemas Distribuidos en 2024.
