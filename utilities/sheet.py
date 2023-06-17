import logging
from typing import Union, Literal, Optional, Sequence

from pandas import DataFrame, read_excel
from pathlib import Path
import settings

logger = logging.getLogger(__name__)


def import_sheet(name: Literal['panels', 'compact-panels', 'accessories']) -> Optional[Union[int, str]]:
    """
    Retrieves the sheet name associated with a given key from the settings.

    This function looks up the provided name in the settings.EXCEL_PATTERN dictionary,
    and logs the retrieved sheet_name. If the sheet_name is a list, it returns the first
    element of the list, otherwise it returns the sheet_name as is.

    :param name: A literal representing the key to look up in the settings.EXCEL_PATTERN dictionary.
    :return: The sheet name associated with the given key. If it's a list, the first element
             is returned. If the key is not found or 'sheet_name' is not in the retrieved dictionary,
             None is returned.
    """
    sheet_info = settings.EXCEL_PATTERN.get(name, {})
    sheet_name = sheet_info.get('sheet_name')

    logger.info(msg=f"Getting sheet: {sheet_name}")

    if isinstance(sheet_name, list):
        return sheet_name[0]

    return sheet_name


def import_columns(name: Literal['panels', 'compact-panels', 'accessories']) -> int | Sequence[int]:
    """
    Retrieves the columns associated with a given key from the settings.

    This function looks up the provided name in the settings.EXCEL_PATTERN dictionary
    and retrieves the 'columns' field from the resulting dictionary.

    :param name: A string that must be one of 'panels', 'compact-panels', or 'accessories',
                 representing the key to look up in the settings.EXCEL_PATTERN dictionary.
    :return: A list containing the columns associated with the given key, or None if the key
             is not found or 'columns' is not in the retrieved dictionary.
    """
    return settings.EXCEL_PATTERN.get(name).get('columns')


def get_valid_table(data_frame: DataFrame, column_name: Union[str, int] = 'REF PEÇA (A)') -> DataFrame:
    """
    Cleans the given DataFrame by dropping rows where the specified column is NaN
    and filling other NaN values with an empty string.

    If column_name is an integer, it is treated as a column index. If it is a string,
    it is treated as a column label. If the column_name is invalid, an error is logged
    and the original DataFrame is returned.

    :param data_frame: The input DataFrame to be cleaned.
    :param column_name: The name or index of the column to be checked for NaN values.
                        Default is 'REF PEÇA (A)'.
    :return: A new DataFrame with rows dropped where the specified column is NaN and other
             NaN values filled with an empty string.
    """
    if isinstance(column_name, int):
        try:
            column_name = data_frame.columns[column_name]
        except IndexError:
            logger.error("Column index out of range.")
            return data_frame

    if column_name not in data_frame.columns:
        logger.error("The table doesn't have the column specified!")
        return data_frame

    return data_frame.dropna(axis=0, subset=[column_name]).fillna('')


def get_data_frame(path: str | Path, sheet_name: Literal['panels', 'compact-panels', 'accessories']) -> Optional[DataFrame]:
    """
    Reads an Excel file and returns a cleaned DataFrame with valid data.

    This function reads an Excel file from the given path and sheet name. It retrieves
    the sheet and columns to be used via helper functions. The resulting DataFrame is
    cleaned by dropping rows where the first column is NaN and filling other NaN values
    with an empty string.

    :param path: The file path to the Excel file as a string or a Path object.
    :param sheet_name: The name of the sheet within the Excel file to read.
    :return: A cleaned DataFrame containing the data read from the specified Excel sheet,
             or None if the sheet name is invalid.
    """
    sheet = import_sheet(sheet_name)
    columns = import_columns(sheet_name)

    if sheet is None:
        logger.error(f"Invalid sheet name: {sheet_name}")
        return None
    try:
        if columns is not None:
            data_frame = read_excel(path, sheet, header=0, usecols=columns,  engine="openpyxl")
        else:
            data_frame = read_excel(path, sheet, header=0,  engine="openpyxl")

        return get_valid_table(data_frame=data_frame, column_name=0,)
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return None


