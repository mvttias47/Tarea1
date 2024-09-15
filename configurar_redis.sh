#!/bin/bash


containers=("redis1" "redis2" "redis3" "redis4")


for container in "${containers[@]}"; do
  echo "Configurando $container..."
  docker exec -it $container redis-cli CONFIG SET maxmemory 500mb
  
done

echo "Configuración completada en todas las particiones."
