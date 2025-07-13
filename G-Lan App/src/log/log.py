import logging
import time

def configurar_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("steam_clone.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

def barra_descarga_simulada():
    total = 20
    print("Iniciando descarga...")
    for i in range(total + 1):
        if i % 4 == 0 or i == total:
            porcentaje = int((i / total) * 100)
            barra = '[' + '#' * i + '-' * (total - i) + ']'
            print(f'Descargando: {barra} {porcentaje}%')
        time.sleep(0.5)  # Más lento para que se note
    print("Descarga completada!")

def descarga_con_barra(id_usuario, descargar_juego_func):
    print('=== Descargar Juego ===')
    try:
        id_juego = int(input("Ingrese el ID del juego que desea descargar: "))
        print("[INFO] Puedes seguir usando el menú mientras se descarga. Los mensajes pueden mezclarse.")
        barra_descarga_simulada()
        descargar_juego_func(id_usuario, id_juego)
        print('\n[INFO] Descarga finalizada.')
    except ValueError:
        print("ID inválido. Por favor, ingrese un número válido.")
    except Exception as e:
        print(f"Error: {e}")