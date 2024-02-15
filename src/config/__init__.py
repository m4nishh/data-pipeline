from dotenv import load_dotenv
import os
from utils.logger import logger

ENV_PATH = "/Users/manishkumar/Desktop/myProjects/data-pipeline/src/environment/.env"

load_dotenv(ENV_PATH)

mandatory_envs = [
    "OPENAI_API_KEY",
    "AWS_REGION",
    "SQSCONSUMER_QUEUENAME"
]
print("openai_key : "+mandatory_envs[0]);

def ensure_envvars():
    """Ensure that these environment variables are provided at runtime"""
    required_envvars = [
        "AWS_REGION",
        "DASH_SQSCONSUMER_QUEUENAME",
        "DATA_PIP_SQSCONSUMER_QUEUENAME"
    ]
    logger.info("loading env")
    missing_envvars = []
    for required_envvar in required_envvars:
        if not os.environ.get(required_envvar, ''):
            missing_envvars.append(required_envvar)

    if missing_envvars:
        message = "Required environment variables are missing: " + \
            repr(missing_envvars)
        raise AssertionError(message)


class AppConfig:
    open_api_key: str
    dash_sqs_consumer_queue_name: str
    data_pip_sqs_consumer_queue_name: str
    db_name: str
    db_host: str
    db_user: str
    db_password: str

    def __init__(self) -> None:
        self.open_api_key = os.environ["OPENAI_API_KEY"]
        self.dash_sqs_consumer_queue_name = os.environ["DASH_SQSCONSUMER_QUEUENAME"]
        self.data_pip_sqs_consumer_queue_name = os.environ["DATA_PIP_SQSCONSUMER_QUEUENAME"]
        self.db_name = os.environ["DB_NAME"]
        self.db_host = os.environ["DB_HOST"]
        self.db_user = os.environ["DB_USER"]
        self.db_password = os.environ["DB_PASSWORD"]

ensure_envvars()
APP_CONFIG = AppConfig()
