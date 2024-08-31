import schedule
import time
from threading import Thread
from update_cryto_currencies import main  
import logging 

logging.basicConfig(filename='scheduler.log', level=logging.INFO)

def job():
    try:
        logging.info("Ejecutando script...")
        thread = Thread(target=main)
        thread.start()
        thread.join()
        logging.info("Ejecución completada.")
    except Exception as e:
        logging.error(f"Error durante la ejecución: {e}")

# Programa la ejecución del script cada 5 minutos
schedule.every(5).minutes.do(job)

logging.info("Scheduler iniciado. Ejecutando el script cada 5 minutos.")

while True:
    try:
        schedule.run_pending()
    except Exception as e:
        logging.error(f"Error en el scheduler: {e}")
    time.sleep(1)  # Espera 1 segundo antes de volver a verificar