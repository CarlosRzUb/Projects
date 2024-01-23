import requests
from discord_webhook import DiscordWebhook
import datetime
import time
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(script_directory, 'ultimafecha.txt')

# Tu clave de API (necesaria para obtener las versiones desde la API de Data Dragon)
api_key = 'RGAPI-991faad4-a205-481f-8a6e-e5990aac8e90'

# Enlace del webhook de Discord
webhook_url = 'https://discord.com/api/webhooks/1175075842775318649/sQ5TwJJ16k9vr7IzDJqBT95eKZVH1NnnDIjzVoq_MBNdALQgQ0pILUFbWYue6iVwX1UD'

def obtener_ultima_version(api_key):
    # Obtener la lista de versiones disponibles desde la API de Data Dragon
    url_api = 'https://ddragon.leagueoflegends.com/api/versions.json'
    headers = {'X-Riot-Token': api_key}  # Agregar el encabezado con la clave de API
    response = requests.get(url_api, headers=headers)

    # Verificar si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        versiones_disponibles = response.json()

        # La última versión es la primera de la lista, eliminando ".1" si está presente
        ultima_version = versiones_disponibles[0].replace(".1", "")
        return ultima_version.replace(".", "-")

    print(f'Error al obtener la versión desde la API de Data Dragon. Código de estado: {response.status_code}')
    return None

def enviar_mensaje_discord(webhook_url, version_actual):
    mensaje = f'¡Nuevas notas del parche disponibles para la versión {version_actual}!'

    # Emojis personalizados de League of Legends
    emoji_league_of_legends = "<:league_of_legends:ID_DEL_EMOJI>"
    emoji_otro_ejemplo = "<:otro_ejemplo:ID_DEL_OTRO_EMOJI>"

    enlace_notas = f'https://www.leagueoflegends.com/es-es/news/game-updates/patch-{version_actual}-notes/'

    # Crear el mensaje con un botón que contiene el enlace a las notas del parche
    mensaje_discord = {
        "content": mensaje,
        "embeds": [
            {
                "title": f"Notas del Parche {version_actual} {":exploding_head:"}",
                "description": "¡Descubre las últimas novedades y cambios en League of Legends! "
                               f"{":punch:"}",
                "url": enlace_notas,
                "color": 3447003,  # Color en formato decimal (puedes usar herramientas en línea para obtenerlos)
                "thumbnail": {
                    "url": "https://www.leagueoflegends.com/static/logo-1200-04b3cefafba917c9c571f9244fd28a1e.png"  # URL de la imagen en miniatura
                },
                "footer": {
                    "text": "League of Legends Patch Notes",
                    "icon_url": "https://static.wikia.nocookie.net/leagueoflegendsoficial/images/d/d2/League_of_legends_logo.png/revision/latest/scale-to-width-down/250?cb=20191021173733&path-prefix=es"  # URL del icono del pie de página
                }
            }
        ]
    }

    # Enviar el mensaje a Discord utilizando el webhook
    webhook = DiscordWebhook(url=webhook_url, **mensaje_discord)
    webhook.execute()

def es_miercoles_par():
    # Obtener el día actual
    now = datetime.datetime.now()
    dia_actual = now.weekday()  # 0 es lunes, 1 es martes, ..., 6 es domingo

    # Verificar si es miércoles (2 en la notación de Python para días de la semana) y si el número de semana es par
    return dia_actual == 2 and now.isocalendar()[1] % 2 == 0

def obtener_fecha_actual():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")  # Formato de fecha YYYY-MM-DD

def obtener_fecha_ultimo_envio():
    try:
        with open(ruta_archivo, "r") as archivo:
            fecha = archivo.read()
            return fecha
    except FileNotFoundError:
        return None

def actualizar_fecha_ultimo_envio(fecha):
    # Borrar la fecha anterior si existe
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)

    # Escribir la nueva fecha
    with open(ruta_archivo, "w") as archivo:
        archivo.write(fecha)

if __name__ == "__main__":
    try:
        # Verificar si es miércoles par
        if es_miercoles_par():
            # Obtener la fecha actual
            fecha_actual = obtener_fecha_actual()

            # Verificar si ya se envió el mensaje hoy
            if fecha_actual != obtener_fecha_ultimo_envio():
                # Obtener la última versión desde la API de Data Dragon
                version_actual = obtener_ultima_version(api_key)

                # Verificar si la versión es válida
                if version_actual:
                    print(f'Nueva versión detectada: {version_actual}')

                    # Enviar el mensaje a Discord con el botón y detalles adicionales
                    enviar_mensaje_discord(webhook_url, version_actual)

                    # Actualizar la fecha del último envío
                    actualizar_fecha_ultimo_envio(fecha_actual)

    except Exception as e:
        print(f'Error inesperado: {str(e)}')