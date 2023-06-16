import logging.config

import settings

logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)

path = "/home/iaggo/Documents/Eins/WoodWorkProjectWatcher/media/public/mofreitas/clientes/iaggo.capitanio@gmail.com/Chanut/briefing/Listas de Corte e Etiquetas/CHANUT_BAR.xlsx"
# def process_event(event_type, event):
#     print(event, event_type)


