import os
import dotenv
from sqlalchemy import create_engine


def database_connection_url():
    dotenv.load_dotenv()
    return os.environ.get("POSTGRES_URI")

    # deployment_type = os.environ.get("DEPLOYMENT_TYPE")
    # if deployment_type == "development":
    #     return os.environ.get("DEVELOPMENT_CONNECTION_URI")
    # return os.environ.get("CONNECTION_URI")


engine = create_engine(database_connection_url(), pool_pre_ping=True)
