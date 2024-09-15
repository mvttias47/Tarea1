from concurrent import futures
import grpc
import cache_system.grpc_service.cache_pb2 as cache_pb2
import cache_system.grpc_service.cache_pb2_grpc as cache_pb2_grpc
import redis
import hashlib
import subprocess
import time
import numpy as np

# Conexión a las particiones de Redis (4 particiones)
redis_partitions = [
    redis.Redis(host='localhost', port=6379),
    redis.Redis(host='localhost', port=6380),
    redis.Redis(host='localhost', port=6381),
    redis.Redis(host='localhost', port=6382),
    redis.Redis(host='localhost', port=6383),
    redis.Redis(host='localhost', port=6384),
    redis.Redis(host='localhost', port=6385),
    redis.Redis(host='localhost', port=6386)
]

# Contador de peticiones por partición
partition_request_counts = [0] * len(redis_partitions)

# Función para realizar la resolución DNS usando 'dig'
def resolve_dns(query):
    result = subprocess.run(['dig', '+short', query], stdout=subprocess.PIPE)
    return result.stdout.decode().strip()

# Particionamiento por hash
def get_partition_by_hash(key):
    partition_number = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(redis_partitions)
    return partition_number, redis_partitions[partition_number]

class CacheService(cache_pb2_grpc.CacheServiceServicer):
    hit_count = 0
    miss_count = 0
    response_times = []

    def GetValue(self, request, context):
        start_time = time.time()

        # Seleccionar partición usando particionamiento por hash
        partition_number, partition = get_partition_by_hash(request.key)
        partition_request_counts[partition_number] += 1
        
        value = partition.get(request.key)
        if value:
            CacheService.hit_count += 1
            status = "HIT"
        else:
            CacheService.miss_count += 1
            resolved_ip = resolve_dns(request.key)
            if resolved_ip:
                
                partition.setex(request.key, 60, resolved_ip)
            status = "MISS" if resolved_ip else "NOT FOUND"

        end_time = time.time()
        response_time = end_time - start_time
        CacheService.response_times.append(response_time)

        return cache_pb2.CacheResponse(value=value.decode() if value else resolved_ip, status=status)


    @staticmethod
    def print_metrics():
        average_response_time = np.mean(CacheService.response_times)
        std_dev_response_time = np.std(CacheService.response_times)
        print(f"Hit Contador: {CacheService.hit_count}")
        print(f"Miss Contador: {CacheService.miss_count}")
        print(f"Hit/Miss Ratio: {CacheService.hit_count / (CacheService.hit_count + CacheService.miss_count):.2f}")
        print(f"Promedio Tiempo de Respuesta: {average_response_time:.6f} seconds")
        print(f"Desviacion Estandar Tiempo de Respuesta: {std_dev_response_time:.6f} seconds")
        print(f"Balance de Carga (Peticiones por Partición):")
        for i, count in enumerate(partition_request_counts):
            print(f"  Partición {i+1}: {count} peticiones")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_pb2_grpc.add_CacheServiceServicer_to_server(CacheService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        CacheService.print_metrics()

if __name__ == '__main__':
    serve()
