import wmi
import requests
import json
import socket
import uuid
import win32evtlog
import subprocess

def obtener_info_sistema():
    c = wmi.WMI()
    sistema = c.Win32_OperatingSystem()[0]
    info_sistema = {
        "Nombre_SO": sistema.Caption,
        "Versión_SO": sistema.Version,
        "IP": socket.gethostbyname(socket.gethostname()),
        "MAC": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    }
    return info_sistema

def obtener_info_antivirus():
    c = wmi.WMI()
    antivirus_info = []
    for antivirus in c.Win32_Product():
        if "antivirus" in antivirus.Caption.lower():
            info = {
                "Nombre": antivirus.Caption,
                "Versión": antivirus.Version,
                "Estado": "Actualizado" if antivirus.InstallDate else "No actualizado"
            }
            antivirus_info.append(info)
    return antivirus_info

def mostrar_trazas_antivirus():
    server = 'localhost'
    logtype = 'Application'
    hand = win32evtlog.OpenEventLog(server, logtype)
    
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    trazas = []
    for event in events:
        if "antivirus" in str(event.StringInserts).lower():
            traza = {
                "Evento_ID": event.EventID,
                "Fuente": event.SourceName,
                "Tiempo_generado": str(event.TimeGenerated),
                "Descripción": event.StringInserts
            }
            trazas.append(traza)
    return trazas

def obtener_puertos_usb():
    resultado = subprocess.run(['powershell', '-Command', 'Get-PnpDevice -Class USB | Select-Object -Property FriendlyName, Status'], capture_output=True, text=True)
    puertos_usb = resultado.stdout.strip().split('\n')
    return puertos_usb

def enviar_info_al_servidor(info):
    url = "http://tu-servidor-web.com/api/sistema"  # Reemplaza con la URL de tu servidor
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(info), headers=headers)
    if response.status_code == 200:
        print("Información enviada exitosamente")
    else:
        print(f"Error al enviar la información: {response.status_code}")

if __name__ == "__main__":
    info_sistema = obtener_info_sistema()
    info_antivirus = obtener_info_antivirus()
    trazas_antivirus = mostrar_trazas_antivirus()
    puertos_usb = obtener_puertos_usb()
    
    info_completa = {
        "Sistema": info_sistema,
        "Antivirus": info_antivirus,
        "Trazas_Antivirus": trazas_antivirus,
        "Puertos_USB": puertos_usb
    }
    
    enviar_info_al_servidor(info_completa)

#tener instaladdo wmi pywin32 y requests