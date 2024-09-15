import grpc
import cache_system.grpc_service.cache_pb2 as cache_pb2
import cache_system.grpc_service.cache_pb2_grpc as cache_pb2_grpc
import csv
from collections import Counter
import matplotlib.pyplot as plt

# Función para cargar dominios desde el archivo CSV sin considerar la frecuencia
# Función para cargar dominios desde el archivo CSV considerando la frecuencia
def load_domains_from_csv(filepath, domain_limit=100):
    domains = []
    with open(filepath, newline='') as csvfile:
        domain_reader = csv.reader(csvfile)
        next(domain_reader)  # Saltar la primera fila de encabezados
        for i, row in enumerate(domain_reader):
            if i >= domain_limit:
                break
            domain = row[0]  # Primera columna contiene los dominios de segundo nivel
            frequency = int(row[1])  # Segunda columna contiene la frecuencia de dominios
            domains.extend([domain] * frequency)  # Añadir el dominio tantas veces como indica la frecuencia
    print(f"{len(domains)} total solicitudes generadas.")
    return domains


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = cache_pb2_grpc.CacheServiceStub(channel)
        
        # Cargar dominios desde el dataset CSV, sin considerar la frecuencia
        test_keys = load_domains_from_csv('data/Statistics table for second-level domains.csv', domain_limit=5)
        
        # Contabilizar las solicitudes para cada dominio
        request_counter = Counter()
        
        # Realizar solicitudes para los dominios cargados
        for key in test_keys:
            request_counter[key] += 1
            print(f"Requesting value for domain: {key}")
            response = stub.GetValue(cache_pb2.CacheRequest(key=key))
            print(f"Get Value: {key} -> {response.value} (Status: {response.status})")
        
        # Mostrar gráfico de la distribución de frecuencias
        plt.figure(figsize=(15, 6))
        plt.bar(request_counter.keys(), request_counter.values())
        plt.xlabel('Dominio')
        plt.ylabel('Frecuencia de Consultas')
        plt.title('Distribución de Frecuencias de Consultas del Dataset')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('consulta_frecuencia_ajustada.png')
        print("El gráfico se ha guardado como 'consulta_frecuencia_ajustada.png'.")

if __name__ == '__main__':
    run()
