from pymongo import MongoClient
from pymongo.server_api import ServerApi

import configparser
from pathlib import Path


def get_mongodb():
    # config parcer
    config = configparser.ConfigParser()

    path_to_file = Path(__file__).parent.joinpath("utils/config_mongodb.ini")
    config.read(path_to_file)

    mongo_user = config.get("DB", "user")
    mongodb_pass = config.get("DB", "pass")
    address = config.get("DB", "address")
    db_name = config.get("DB", "db_name")

    uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{address}/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi("1"))
    db = client[db_name]

    return db
