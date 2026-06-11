from core.clients import Client
from core.config import Config
from ingest.pipeline import ingest


def main():

    config = Config.load("./config.toml")
    clients = Client(config)
    ingest(config, clients)


if __name__ == "__main__":
    main()
