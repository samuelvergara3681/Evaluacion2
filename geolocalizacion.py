import urllib.parse
import requests

# API Key de Graphhopper Directions (Reemplaza con tu token personal)
API_KEY = "9d5fdbd5-6fb9-40d6-9ab3-82aad926861b"

# Endpoints oficiales de Graphhopper
GEOCODE_API = "https://graphhopper.com/api/1/geocode?"
ROUTE_API = "https://graphhopper.com/api/1/route?"

def obtener_coordenadas(ubicacion):
    """
    Obtiene la latitud, longitud y nombre formateado de una ubicación.
    """
    params = {
        "q": ubicacion,
        "limit": "1",
        "key": API_KEY
    }
    url = GEOCODE_API + urllib.parse.urlencode(params)
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        json_data = respuesta.json()
        if json_data.get("hits"):
            punto = json_data["hits"][0]
            lat = punto["point"]["lat"]
            lng = punto["point"]["lng"]
            nombre = punto["name"]
            pais = punto.get("country", "")
            nombre_completo = f"{nombre}, {pais}" if pais else nombre
            return lat, lng, nombre_completo
    return None, None, None

def calcular_ruta(lat1, lng1, lat2, lng2):
    """
    Consulta la API de rutas de Graphhopper con la narrativa en español (locale=es).
    """
    params = [
        ("point", f"{lat1},{lng1}"),
        ("point", f"{lat2},{lng2}"),
        ("vehicle", "car"),
        ("locale", "es"),  # Forzar narrativa en español
        ("key", API_KEY)
    ]
    url = ROUTE_API + urllib.parse.urlencode(params)
    return requests.get(url)

# -------------------------------------------------------------
# Programa Principal
# -------------------------------------------------------------
print("==================================================")
print("     SISTEMA DE GEOLOCALIZACIÓN Y RUTAS           ")
print("==================================================")

while True:
    print("\n--------------------------------------------------")
    # Entrada de origen con validación de salida
    origen = input("Ingrese la ciudad/punto de origen (o 's' / 'salir' para finalizar): ").strip()
    if origen.lower() in ["s", "salir"]:
        print("\n¡Gracias por utilizar el servicio de geolocalización! Hasta luego.")
        break

    # Entrada de destino con validación de salida
    destino = input("Ingrese la ciudad/punto de destino (o 's' / 'salir' para finalizar): ").strip()
    if destino.lower() in ["s", "salir"]:
        print("\n¡Gracias por utilizar el servicio de geolocalización! Hasta luego.")
        break

    print("\nObteniendo coordenadas y calculando ruta...")
    
    # Obtener coordenadas de origen y destino
    lat_origen, lng_origen, nombre_origen = obtener_coordenadas(origen)
    lat_destino, lng_destino, nombre_destino = obtener_coordenadas(destino)

    if not lat_origen or not lat_destino:
        print(" Error: No se pudo encontrar una o ambas ubicaciones. Por favor intente nuevamente.")
        continue

    # Consultar ruta
    respuesta_ruta = calcular_ruta(lat_origen, lng_origen, lat_destino, lng_destino)

    if respuesta_ruta.status_code == 200:
        json_ruta = respuesta_ruta.json()
        path = json_ruta["paths"][0]
        
        # Extracción y conversión de datos
        distancia_km = path["distance"] / 1000.0  # Convertir metros a kilómetros
        tiempo_min = path["time"] / 1000.0 / 60.0  # Convertir milisegundos a minutos

        print("\n==================================================")
        print("RESUMEN DEL VIAJE")
        print("==================================================")
        print(f"Origen  : {nombre_origen}")
        print(f"Destino : {nombre_destino}")
        # Formato numérico con máximo dos decimales (:.2f)
        print(f"Distancia total : {distancia_km:.2f} km")
        print(f"Tiempo estimado : {tiempo_min:.2f} minutos")
        print("--------------------------------------------------")
        print("NARRATIVA DEL VIAJE (INDICACIONES PASO A PASO):")
        print("--------------------------------------------------")

        # Imprimir narrativa paso a paso
        instrucciones = path.get("instructions", [])
        for i, paso in enumerate(instrucciones, start=1):
            texto = paso.get("text", "")
            dist_paso_km = paso.get("distance", 0) / 1000.0
            # Cada paso impreso en español con distancia formateada a 2 decimales
            print(f"{i}. {texto} ({dist_paso_km:.2f} km)")
            
    else:
        print(f" Error al calcular la ruta. Código HTTP: {respuesta_ruta.status_code}")