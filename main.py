from core.config import Config
from ingest.pipeline import ingest


def main():

    config = Config.load("./config.toml")
    ingest(config)


if __name__ == "__main__":
    main()
