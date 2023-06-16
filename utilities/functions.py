import datetime
import logging
from pathlib import Path
from typing import Union, Optional
from pandas import DataFrame
import pandas as pd
from payload import PartPayload
import settings
from payload import ConsumablePayload

logger = logging.getLogger(__name__)

file = "/home/iaggo/Documents/Eins/WoodWorkProjectWatcher/media/public/mofreitas/clientes/iaggo.capitanio@gmail.com/Chanut/briefing/Listas de Corte e Etiquetas/CHANUT_BAR.xlsx"


def validate_path(path: Union[str, Path]) -> Path:
    if isinstance(path, str):
        path = Path(path)
    return path.resolve()


def verify(source_path: Path) -> bool:
    """
    Verifies if the given source path contains the specified reference as one of its parts and
    if it is not a directory.

    This function takes a path and a reference string as input. It first checks if the source_path
    is a directory, and if so, returns False. It then checks if the reference string is part of the path.
    If it is, the function traverses up the path to confirm if any part of the path matches the reference string.

    :param source_path: A Path object representing the source path to be verified.
    :param reference: A string representing the reference to be checked in the source path.
                      Default is 'Lists_and_Tags'.
    :return: True if the source path contains the reference and is not a directory, False otherwise.
    """
    if source_path.is_dir():
        return False
    if settings.CUT_LIST_DIR not in source_path.parts:
        return False
    current_path = Path(*source_path.parts[source_path.parts.index(settings.CUT_LIST_DIR):])
    while current_path != current_path.parent:  # Stop when reaching the root directory
        if current_path.name == settings.CUT_LIST_DIR:
            return True
        current_path = current_path.parent
    return False


def get_email(path: Union[str, Path]) -> str:
    path = validate_path(path)
    return path.parts[path.parts.index(settings.KEYWORD) + 1]


def get_budget_name(path: Union[str, Path]) -> str:
    path = validate_path(path)
    return path.parts[path.parts.index(settings.KEYWORD) + 2]


def get_path_after_keyword(path: Union[str, Path]) -> Optional[Path]:
    try:
        logger.info(f"Trying to get reference path after keyword {settings.KEYWORD}: {path}")
        path = validate_path(path)
        path = Path(*path.parts[path.parts.index(settings.KEYWORD):])
        return path
    except Exception as error:
        logger.error(f"Error: Unable to retrieve the relative path. \n"
                     f"The event may have been triggered outside the reference path. {error}")


def generate_id(name: str, object_type: str = 'Part') -> str:
    return f'urn:ngsi-ld:{object_type}:{name}'


def check(string: str) -> bool:
    return string in ("CNC", "X")


def consumable_accessories_payload(data_frame: pd.DataFrame, belongs_to: str, **kwargs):
    observed_at = kwargs.get("observed_at", datetime.datetime.utcnow().isoformat())

    for _, row in data_frame.iterrows():
        name, mat, quant, obs = row
        identifier = generate_id(name, object_type='Part')
        consumable = ConsumablePayload(id=identifier, name=name, amount=quant, status=0, belongsTo=belongs_to)

        logger.debug(f"Extracting form excel the values: {identifier, name, mat, quant, obs, belongs_to, observed_at}")

        response = consumable.post()
        logger.debug(f"Response Status Code: {response.status_code}")
        if response != 201:
            response = consumable.patch()
            logger.debug(f"Response Status Code: {response.status_code}")


def create_payload_and_send(data_frame: DataFrame, payload_class, belongs_to: str, order_by: str = None, **kwargs):
    """
    Helper function to create payloads and send them to a context broker.

    :param data_frame: DataFrame containing data.
    :param payload_class: Class to create payload objects.
    :param belongs_to: Information on what the data belongs to.
    :param order_by: Specifies the order in which the data should be processed.
    :param kwargs: Additional keyword arguments for payload class.
    """
    for _, row in data_frame.iterrows():
        payload_params = {"belongsTo": belongs_to}
        if order_by:
            payload_params["orderBy"] = order_by

        for key, value in kwargs.items():
            payload_params[key] = value

        for col_name, col_value in zip(data_frame.columns, row):
            payload_params[col_name] = col_value

        payload = payload_class(**payload_params)
        logger.debug(f"Trying to post payload: {payload_params}")

        response = payload.post()
        logger.debug(f"Response Status Code: {response.status_code}")

        if response.status_code != 201:
            logger.debug(f"Trying to patch payload...")
            response = payload.patch()
            logger.debug(f"Response Status Code: {response.status_code}")
            logger.info(f"Response text : {response.text}")


def part_panels_payload(data_frame: DataFrame, belongs_to: str, **kwargs):
    """
    Extract the panels from the provided DataFrame and sends payloads to a context broker.

    :param data_frame: DataFrame containing panel data.
    :param belongs_to: Information on what the panels belong to.
    :param orderBy: Specifies the order in which the panels should be processed.
    :param kwargs: Additional keyword arguments for the PartPayload.
    """
    create_payload_and_send(data_frame, PartPayload, belongs_to, **kwargs)


def part_compact_panels_payload(data_frame: DataFrame, belongs_to: str, order_by: str, **kwargs):
    """
    Extract the compact panels from the provided DataFrame and sends payloads to a context broker.

    :param data_frame: DataFrame containing compact panel data.
    :param belongs_to: Information on what the compact panels belong to.
    :param order_by: Specifies the order in which the compact panels should be processed.
    :param kwargs: Additional keyword arguments for the PartPayload.
    """
    create_payload_and_send(data_frame, PartPayload, belongs_to, order_by, **kwargs)


def consumable_accessories_payload(data_frame: DataFrame, belongs_to: str, **kwargs):
    """
    Extract the consumable accessories from the provided DataFrame and sends payloads to a context broker.

    :param data_frame: DataFrame containing consumable accessory's data.
    :param belongs_to: Information on what the consumable accessories belong to.
    :param kwargs: Additional keyword arguments for the ConsumablePayload.
    """
    observed_at = kwargs.pop("observed_at", datetime.datetime.utcnow().isoformat())
    create_payload_and_send(data_frame, ConsumablePayload, belongs_to, None, observed_at=observed_at, **kwargs)


def create_part(path: str):
    file_path = validate_path(path)
    if verify(source_path=file_path):
        file_name = file_path.stem.upper().strip()
        budget = get_budget_name(path).upper().strip()
        furniture = file_name.replace(budget, '').replace(' ', '').strip('_')



if __name__ == "__main__":

    create_part(file)
