import logging.config
import queue
import threading
import time

from watchdog.observers import Observer

import settings
from utilities import http_request as http, handler

logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Queues and Sets
    event_queue = queue.Queue()
    delayed_scan_queue = queue.Queue()
    directories_in_queue = set()

    http.test_connection()

    # Threads
    worker_thread = threading.Thread(target=handler.worker, args=(event_queue,))
    delayed_scan_thread = threading.Thread(target=handler.delayed_scan_worker,
                                           args=(event_queue, delayed_scan_queue, directories_in_queue))

    worker_thread.start()
    delayed_scan_thread.start()

    # Watchdog
    logger.info(f"Watching DIR: {settings.WATCHING_DIR}")
    event_handler = handler.ExcelEventHandler(event_queue, delayed_scan_queue, directories_in_queue)
    observer = Observer()
    observer.schedule(event_handler, path=settings.WATCHING_DIR, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(settings.SLEEP_DURATION)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # Stop worker thread
    event_queue.put(None)
    worker_thread.join()
