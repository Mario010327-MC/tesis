import platform # Importa la biblioteca platform, que proporciona información sobre el sistema operativo
import psutil # Importa la biblioteca psutil, que permite acceder a detalles sobre el hardware del sistema
import os # Importa la biblioteca os, que proporciona funciones para interactuar con el sistema operativo

def get_system_info():
    os_type = platform.system() # Obtiene el tipo de sistema operativo (Windows, Linux, etc.)

    # Si el sistema operativo es Windows
    if os_type == "Windows":
        # Obtiene la versión de Windows, combinando el número de versión y la versión detallada
        win_version = platform.release() + " " + platform.version()
        info = {
            "Sistema Operativo": os_type, # Tipo de sistema operativo
            "Versión de Windows": win_version, # Versión específica de Windows
            "Nombre del Nodo": platform.node(), # Nombre de la máquina en la red
            "Arquitectura del SO": platform.machine(), # Arquitectura del sistema operativo (por ejemplo, x86_64)
            "Procesador": platform.processor(), # Información sobre el procesador
            "Memoria Total (GB)": round(psutil.virtual_memory().total / (1024**3), 2), # Memoria RAM total en GB
            "Uso de CPU (%)": psutil.cpu_percent(interval=1), # Porcentaje de uso de CPU en el último segundo
            "Dirección IP": psutil.net_if_addrs()['Wi-Fi'][1].address, # Dirección IP de la interfaz de red Wi-Fi
            "Disco Total (GB)": round(psutil.disk_usage('/').total / (1024**3), 2), # Espacio total en el disco en GB
            "Espacio Libre en Disco (GB)": round(psutil.disk_usage('/').free / (1024**3), 2) # Espacio libre en el disco en GB
        }
    # Si el sistema operativo es Linux
    elif os_type == "Linux":
        info = {
            "Sistema Operativo": os_type, # Tipo de sistema operativo
            "Distribución de Linux": " ".join(platform.linux_distribution()), # Distribución específica de Linux
            "Nombre del Nodo": platform.node(), # Nombre de la máquina en la red
            "Versión del SO": platform.version(), # Versión específica del sistema operativo
            "Arquitectura del SO": platform.machine(), # Arquitectura del sistema operativo (por ejemplo, x86_64)
            "Procesador": platform.processor(), # Información sobre el procesador
            "Memoria Total (GB)": round(psutil.virtual_memory().total / (1024**3), 2), # Memoria RAM total en GB
            "Uso de CPU (%)": psutil.cpu_percent(interval=1), # Porcentaje de uso de CPU en el último segundo
            "Dirección IP": psutil.net_if_addrs()['wlan0'][0].address, # Dirección IP de la interfaz de red WLAN0
            "Disco Total (GB)": round(psutil.disk_usage('/').total / (1024**3), 2), # Espacio total en el disco en GB
            "Espacio Libre en Disco (GB)": round(psutil.disk_usage('/').free / (1024**3), 2) # Espacio libre en el disco en GB
        }

    # Imprime la información recopilada
    for key, value in info.items():
        print(f"{key}: {value}")

    return info

def save_info_to_file(info, file_path):
    with open(file_path, 'w') as file:
        for key, value in info.items():
            file.write(f"{key}: {value}\n")

if __name__ == "__main__":
    system_info = get_system_info() # Recopila la información del sistema
    #save_info_to_file(system_info, "~/Documents/system_info.txt") # Guarda la información en la ruta especificada
    input("Presiona Enter para salir...") # Pausa para mantener la ventana abierta