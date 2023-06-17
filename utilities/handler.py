import functools
import os
from pathlib import Path
import logging.config
import time
from watchdog.events import FileCreatedEvent
from watchdog.events import PatternMatchingEventHandler

import settings
from utilities import task

logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)


def worker(event_queue):
    """
    Worker function that processes events from the event queue.

    This function continuously retrieves events from the event queue and processes them using the `task.process_event`
    method. The function breaks the loop and terminates when a `None` value is encountered in the event queue.

    Args:
        event_queue (queue.Queue): The queue from which events are retrieved.

    Returns:
        None

    """
    while True:
        event_tuple = event_queue.get()
        if event_tuple is None:
            break
        event_type, event = event_tuple
        task.process_event(event_type, event)


def delayed_scan_worker(event_queue, delayed_scan_queue, directories_in_queue):
    """
    Verifies if the given source path contains the specified reference as one of its parts and
    if it is not a directory.

    This function takes the following parameters:

    :param event_queue: A queue.Queue object representing the queue to which scan events are added.
    :param delayed_scan_queue: A queue.Queue object representing the queue from which directories scheduled for delayed
    scanning are retrieved.
    :param directories_in_queue: A list containing the directories currently in the queue.

    This function does not return a value.

    """
    directory_timestamps = {}

    while True:
        directory = delayed_scan_queue.get()
        if directory is None:
            break

        current_time = time.time()

        missing_time: float = current_time - directory_timestamps[directory]

        # If the directory is already scheduled for scanning, skip this iteration
        if directory in directory_timestamps and missing_time < settings.DELAY_FOR_SCAN:
            continue

        # Otherwise, update the time it was added to the queue
        directory_timestamps[directory] = current_time

        # Wait 30 seconds
        time.sleep(settings.DELAY_FOR_SCAN)

        # Check if 30 seconds have passed since the directory was first added to the queue
        if time.time() - directory_timestamps[directory] >= settings.DELAY_FOR_SCAN:
            ExcelEventHandler(event_queue, delayed_scan_queue, directories_in_queue).scan_directory(directory)
            directories_in_queue.remove(directory)


class ExcelEventHandler(PatternMatchingEventHandler):
    """
    Event handler for monitoring Excel files with the .xlsx extension.

    This handler is designed to respond to file system events involving Excel files.
    It ignores events related to directories and is not case-sensitive.

    Example usage:
        event_handler = ExcelEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path='path_to_watch', recursive=False)
        observer.start()
    """

    def __init__(self, event_queue, delayed_scan_queue, directories_in_queue, *args, **kwargs):
        patterns = ['*.xlsx']
        super().__init__(patterns=patterns, ignore_directories=True, case_sensitive=False)
        self.event_queue = event_queue
        self.delayed_scan_queue = delayed_scan_queue
        self.directories_in_queue = directories_in_queue

        logger.info(f"------------- PROJECT WATCHER INITIALIZED -------------")

    @staticmethod
    @functools.cache
    def parse_path(path: str) -> Path:
        return Path(path).resolve()

    @functools.cache
    def is_valid_path(self, path: str) -> bool:
        path: Path = self.parse_path(path)
        if path.is_dir():
            return False
        return path.parent.stem.__str__() == settings.CUT_LIST_DIR and path.parent.parent.stem.__str__() == 'briefing'

    @functools.cache
    def add_to_event_queue(self, event):
        logger.info(f"Adding to queue for processing.")
        self.event_queue.put(('created', event))

    @functools.cache
    def add_to_dir_queue(self, path: Path):
        if not path.is_dir():
            path = path.parent
        if path in self.directories_in_queue:
            self.directories_in_queue.add(path)
            self.delayed_scan_queue.put(path)

    def add_to_queue(self, event, msg: str = None):
        if msg is None:
            msg = "'Modified' event triggered for 'file':"
        file_path: Path = self.parse_path(event.src_path)
        dir_path = file_path.parent
        msg += f" {event.src_path}"
        if self.is_valid_path(event.src_path):
            logger.info(msg)
            self.add_to_event_queue(event)
            self.add_to_dir_queue(dir_path)

    def on_modified(self, event):
        self.add_to_queue(event)

    def on_created(self, event):
        self.add_to_queue(event, msg="'Created' event triggered for 'file':")

    def on_moved(self, event):
        self.add_to_queue(event, msg=f"'Moved' event triggered for 'file':")

    # def on_deleted(self, event):
    #     self.add_to_queue(event, msg="'Deleted' event triggered for 'file':")

    def scan_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                path = Path(os.path.join(root, file))
                logger.info(f"Found file: ... {path.parent}/{path.name}")
                event = FileCreatedEvent(path)
                self.event_queue.put(('created', event))
