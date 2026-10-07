import os
import sys
import re

# Obtener la ruta base donde se ejecuta el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("--- ACTUALIZADOR DE FLOW AUTOMÁTICO ---")

# En GitHub Actions leemos la URL desde los Secretos/Variables de entorno
url_nueva = os.environ.get('URL_FLOW', '').strip()

if not url_nueva:
    print("Error: No se encontró la variable de entorno 'URL_FLOW'.")
    print("Asegúrate de agregar la URL en los Secrets de GitHub con la clave 'URL_FLOW'.")
    sys.exit(1)

if "/live/" not in url_nueva:
    print("Error: La URL ingresada no contiene '/live/'.")
    sys.exit(1)

base_nueva_limpia = url_nueva.split("/live/")[0]

print(f"Nueva base de token detectada correctamente.")
print(f"Escaneando archivos M3U/TXT en: {BASE_DIR}")

modificados = 0

for root, dirs, files in os.walk(BASE_DIR):
    if "flow_profile" in root:
        continue
        
    for file in files:
        if file.endswith((".m3u", ".m3u8", ".txt")):
            ruta_archivo = os.path.join(root, file)
            
            with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.read()

            patron = r'https://[^\s"<>]+?/live/'
            contenido_actualizado, count = re.subn(patron, f'{base_nueva_limpia}/live/', contenido)

            if count > 0:
                with open(ruta_archivo, "w", encoding="utf-8") as f:
                    f.write(contenido_actualizado)
                modificados += 1
                print(f"-> ¡Actualizado con éxito: {file} ({count} enlaces modificados)!")

print(f"\n¡Proceso finalizado! Archivos modificados: {modificados}")