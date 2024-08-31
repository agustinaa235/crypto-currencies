import schedule
import time
from threading import Thread
from update_cryto_currencies import main  
import logging 

logging.basicConfig(filename='automation.log', level=logging.INFO)

def job():
    try:
        logging.info("Ejecutando script...")
        thread = Thread(target=main)
        thread.start()
        thread.join()
        logging.info("Ejecución completada.")
    except Exception as e:
        logging.error(f"Error durante la ejecución: {e}")

schedule.every().day.at("08:00").do(job)

logging.info("Scheduler iniciado. Ejecutando el script cada 10 minutos.")

main()

while True:
    try:
        schedule.run_pending()
    except Exception as e:
        logging.error(f"Error en el scheduler: {e}")
    time.sleep(30) 