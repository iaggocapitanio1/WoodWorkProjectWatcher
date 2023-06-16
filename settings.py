from pathlib import Path
from dotenv import load_dotenv
import os


def str_to_bool(target) -> bool:
    if isinstance(target, bool):
        return target
    return target.lower() == 'true'


def mega_bytes_to_bits(mega: int) -> int:
    return mega * 1024 * 1024


load_dotenv()

NAMESPACE = 'PROJECT_WATCHER'

if NAMESPACE:
    NAMESPACE += '_'


def parse_env(string: str) -> str:
    return NAMESPACE + string


BASE_DIR = Path(__file__).resolve().parent

DELAY_FOR_SCAN = 30

NUM_WORKER_THREADS = int(os.environ.get(parse_env("NUM_WORKER_THREADS"), 4))

PATH_REFERENCE = os.environ.get(parse_env("PATH_REFERENCE"), "mofreitas/clientes/")

CLIENT_ID = os.environ.get(parse_env("CLIENT_ID"), "")

CLIENT_SECRET = os.environ.get(parse_env("CLIENT_SECRET"), "")

TOKEN_URL = os.environ.get(parse_env("TOKEN_URL"), "http://localhost:8000/auth/token")

URL = os.environ.get(parse_env("URL"), "http://127.0.0.1:8000/api/v1")

WATCHING_DIR = os.environ.get(parse_env("WATCHING_DIR"), BASE_DIR / '/home/app/media/public/mofreitas')

WATCHING_DIR = Path(WATCHING_DIR).resolve()

NGSI_LD_CONTEXT = os.environ.get(parse_env("NGSI_LD_CONTEXT"), False)

CUT_LIST_DIR = "Listas de Corte e Etiquetas"

KEYWORD = "clientes"

HEADERS = {
    'Content-Type': 'application/json',
    'Fiware-Service': 'woodwork40',
    'Link': f'<{NGSI_LD_CONTEXT}>; rel="http://www.w3.org/ns/json-ld#context;type="application/ld+json"'

}
EXCEL_PATTERN = {
    "panels": {
        "columns": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        # "sheet_name": [6]
        "sheet_name": ['DATA - Paineis']
    },
    "compact-panels": {
        "columns": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],

        # "sheet_name": [9]
        'sheet_name': ['DATA - Macicos']
    },
    "accessories": {
        "columns": [0, 2, 3, 4],
        # "sheet_name": [7]
        'sheet_name': ['DATA - Acessorios']
    }
}

LOG_DIR = BASE_DIR.joinpath('logs')

LOG_DIR.mkdir(exist_ok=True, parents=True)

LOGGER = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - level: %(levelname)s - loc: %(name)s - func: %(funcName)s - msg: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR.joinpath('watch.log'),
            "level": "DEBUG",
            "maxBytes": mega_bytes_to_bits(mega=1),
            "backupCount": 3,
            "formatter": "simple"
        }
    },
    "loggers": {
        "utilities": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "file"
        ],
    }
}
