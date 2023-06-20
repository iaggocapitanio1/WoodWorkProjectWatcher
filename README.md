# WoodWorkProjectWatcher

WoodWorkProjectWatcher is a Python project designed to monitor and manage woodwork projects. The tool extracts data from predefined data sources, processes it, and sends payloads to a context broker.

## Requirements

- Python 3.9 or later.

## Getting Started

Before using the WoodWorkProjectWatcher, ensure that you have Python 3.9 or later installed on your system. You can check your Python version by running:

```sh
python --version
```

If you have an older version of Python, you can download the latest version from the [official Python website](https://www.python.org/downloads/).
## Features

- Monitors a specified directory for changes in Excel files.
- Performs delayed scanning of directories to avoid redundant processing.
- Logs activity to both the console and a file.
- Configuration through environment variables.

### Clone the Repository

Clone this repository to your local machine:

```sh
git clone git@github.com:iaggocapitanio1/WoodWorkProjectWatcher.git
cd WoodWorkProjectWatcher
```


### Set Up a Virtual Environment (optional)

It is a good practice to create a virtual environment for your Python projects. You can create a virtual environment by running:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
## Configuration

The application can be configured using environment variables. You can place these variables in a `.dev.env` file for local development or set them in your environment for production use.

Here is the list of environment variables:

- `PROJECT_WATCHER_DELAY_FOR_SCAN`: The delay in seconds before a directory is scanned. Default is 20 seconds.
- `PROJECT_WATCHER_SLEEP_DURATION`: The sleep duration in seconds between directory polls. Default is 0.3 seconds.
- `PROJECT_WATCHER_NUM_WORKER_THREADS`: Number of worker threads for processing. Default is 4.
- `PROJECT_WATCHER_PATH_REFERENCE`: The reference path to be used for processing. Default is "mofreitas/clientes/".
- `PROJECT_WATCHER_CLIENT_ID`: Client ID for authentication.
- `PROJECT_WATCHER_CLIENT_SECRET`: Client Secret for authentication.
- `PROJECT_WATCHER_TOKEN_URL`: URL for token retrieval. Default is "http://localhost:8000/auth/token".
- `PROJECT_WATCHER_URL`: Base URL for the API. Default is "http://127.0.0.1:8000/api/v1".
- `PROJECT_WATCHER_WATCHING_DIR`: The directory to be monitored. Default is the `BASE_DIR` concatenated with '/home/app/media/public/mofreitas'.
- `PROJECT_WATCHER_NGSI_LD_CONTEXT`: The NGSI-LD context URL.
- `PROJECT_WATCHER_CUT_LIST_DIR`: Directory name for cut lists. Default is "Listas de Corte e Etiquetas".
- `PROJECT_WATCHER_KEYWORD`: Keyword used in processing. Default is "clientes".

### Install Dependencies

Install the required dependencies:

```sh
pip install -r requirements.txt
```

### Running the Application

Run the main script:

```sh
python main.py
```

## Usage

Provide a brief description of how to use the application, including any command-line arguments and options, configuration files, etc.

## Contributing

Explain how others can contribute to your project. For example, how to submit bugs, feature requests, and how to contribute code.

## License

Specify the license under which your project is distributed.

## Contact

Iaggo Capitanio - iaggo.capitanio@gmail.com

Project Link: [https://github.com/iaggocapitanio1/WoodWorkProjectWatcher](https://github.com/iaggocapitanio1/WoodWorkProjectWatcher)




## Acknowledgments

- [Nuno](https://github.com/nunoguedesmore)
