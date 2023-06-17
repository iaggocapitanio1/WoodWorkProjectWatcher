import logging.config
from utilities import functions, sheet
import settings

logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)


def process_event(event_type, event):
    logger.info(f"Event type: {event_type} | Event src_path: {event.src_path}")
    path = functions.validate_path(event.src_path)
    file_name = path.stem.upper().strip()
    budget = functions.get_budget_name(path)
    if not functions.verify(source_path=path):
        return
    if event_type == "delete":
        return
    furniture = functions.get_furniture_name(file=file_name, budget_name=budget)
    project_id = functions.generate_id(name=budget, object_type='Project')
    furniture_id = functions.generate_id(name=furniture, object_type='Furniture')
    panels_dataframe = sheet.get_data_frame(path=path, sheet_name="panels")
    compact_panels_dataframe = sheet.get_data_frame(path=path, sheet_name="compact-panels")
    functions.part_panels_payload(data_frame=panels_dataframe, belongs_to=project_id, belongs_to_furniture=furniture_id)
    functions.part_compact_panels_payload(data_frame=compact_panels_dataframe, belongs_to=project_id,
                                          belongs_to_furniture=furniture_id)
